#!/usr/bin/env python3
"""Plain-assert tests for gitlab_issue.py. Run: python3 test_gitlab_issue.py (or py -3)."""

import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gitlab_issue as g  # noqa: E402


def test_emit_ascii_roundtrip():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        g.emit({"t": "þðæö"})
    out = buf.getvalue()
    assert out.isascii(), out
    assert json.loads(out)["t"] == "þðæö"


def raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


def test_parse_ref():
    for ref in ("#12", "12", "  #12 "):
        assert g.parse_ref(ref) == (12, None, None), ref
    assert g.parse_ref("https://gitlab.example.com/acme/sub/verk/-/issues/12") == (
        12,
        "acme/sub/verk",
        "gitlab.example.com",
    )
    for bad in (
        "fix login",
        "#0",
        "",
        "https://gitlab.example.com/acme/verk/-/merge_requests/3",
    ):
        assert raises(ValueError, g.parse_ref, bad), bad


def test_issue_endpoint():
    assert g.issue_endpoint(12, None, None) == ([], "projects/:fullpath/issues/12")
    assert g.issue_endpoint(12, "acme/sub/verk", "gitlab.example.com") == (
        ["--hostname", "gitlab.example.com"],
        "projects/acme%2Fsub%2Fverk/issues/12",
    )


ISSUE = {
    "iid": 12,
    "title": "Leyfa að merkja verk lokið þegar",
    "description": "Notandi vill haka við verk.",
    "state": "opened",
    "labels": ["feature"],
    "web_url": "https://gitlab.example.com/acme/verk/-/issues/12",
}


def note(i, system=False):
    return {
        "system": system,
        "body": f"comment {i}",
        "created_at": f"2026-01-{i:02d}T10:00:00Z",
        "author": {"username": f"gervi{i}"},
    }


def test_compose():
    # (a) system notes dropped, newest first, no omissions
    r = g.compose(ISSUE, [note(1), note(3, system=True), note(2)])
    d = r["DESCRIPTION"]
    assert "comment 3" not in d
    assert "## Comments (supporting context, newest first)" in d
    assert d.index("@gervi2 (2026-01-02T10:00:00Z):\ncomment 2") < d.index(
        "@gervi1 (2026-01-01T10:00:00Z):"
    )
    assert r["OMITTED_COMMENTS"] == 0
    assert (r["NUMBER"], r["STATE"], r["URL"], r["LABELS"]) == (
        12,
        "opened",
        ISSUE["web_url"],
        ["feature"],
    )
    assert r["EMPTY_DESCRIPTION"] is False
    # (b) no description
    r = g.compose({**ISSUE, "description": None}, [])
    assert "(no description)" in r["DESCRIPTION"] and r["EMPTY_DESCRIPTION"] is True
    # (c) truncation to newest 20
    r = g.compose(ISSUE, [note(i) for i in range(1, 26)])
    assert r["OMITTED_COMMENTS"] == 5
    assert r["DESCRIPTION"].endswith("(5 older comments omitted)")
    assert (
        "comment 25" in r["DESCRIPTION"]
        and "comment 5\n" not in r["DESCRIPTION"] + "\n"
    )
    # (d) no notes, no heading
    assert "## Comments" not in g.compose(ISSUE, [])["DESCRIPTION"]
    # (e) header lines, (f) Icelandic survives
    lines = g.compose(ISSUE, [])["DESCRIPTION"].split("\n")
    assert lines[0] == "GitLab issue #12: Leyfa að merkja verk lokið þegar"
    assert lines[1] == f"Source: {ISSUE['web_url']}"


def test_summarize():
    issues = [
        {"iid": 14, "title": "Þriðja", "labels": ["bug"], "state": "opened"},
        {"iid": 13, "title": "Annað", "labels": [], "state": "opened"},
        {"iid": 11, "title": "Fyrsta", "labels": ["a", "b"], "state": "opened"},
    ]
    assert g.summarize(issues) == {
        "ISSUES": [
            {"NUMBER": 14, "TITLE": "Þriðja", "LABELS": ["bug"]},
            {"NUMBER": 13, "TITLE": "Annað", "LABELS": []},
            {"NUMBER": 11, "TITLE": "Fyrsta", "LABELS": ["a", "b"]},
        ]
    }
    assert g.summarize([]) == {"ISSUES": []}


def test_branch_name():
    assert g.branch_name(12, "Allow marking tasks done") == "12-allow-marking-tasks-done"
    assert g.branch_name(12, "Þýða villuboð á íslensku") == "12-thyda-villubod-a-islensku"
    assert g.branch_name(12, "Bæta við eiganda") == "12-baeta-vid-eiganda"
    assert g.branch_name(12, "Röðun verka") == "12-rodun-verka"
    assert g.branch_name(12, "Fix: login  -- crash on SAVE now please") == "12-fix-login-crash-on"
    assert g.branch_name(12, "!!!") == "12"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("ok")
