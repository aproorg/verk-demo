#!/usr/bin/env python3
"""Fetch a GitLab issue (or list open ones) via `glab api` and print one JSON object.

    gitlab_issue.py view <ref>   # ref: 12, #12, or https://host/group/project/-/issues/12
    gitlab_issue.py list

Stdout is always a single ASCII-only JSON object; errors are {"ERROR", "HINT"} with a
non-zero exit (2 bad ref/usage, 3 glab missing, 4 glab api failed). Stdlib only, 3.9+.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse
from typing import Any, NoReturn


def emit(obj: Any) -> None:
    # ensure_ascii: a cp1252 Windows console can't mangle or choke on þ/ð/æ/ö.
    print(json.dumps(obj, ensure_ascii=True))


def fail(code: int, error: str, hint: str) -> NoReturn:
    emit({"ERROR": error, "HINT": hint})
    sys.exit(code)


def run_glab(args: list[str], what: str = "") -> Any:
    if shutil.which("glab") is None:
        fail(
            3,
            "glab is not installed",
            "Install: brew install glab | winget install GLab.GLab | scoop install glab, "
            "then glab auth login. Or paste the issue text into /speckit-specify.",
        )
    # List args, never shell=True; explicit utf-8 so Windows doesn't decode as cp1252.
    proc = subprocess.run(["glab", "api", *args], capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        fail(
            4,
            what + (proc.stderr.strip() or proc.stdout.strip() or "glab api failed"),
            "Check the issue number and `glab auth status`. "
            "Only GitLab remotes are supported (not GitHub).",
        )
    return json.loads(proc.stdout)


MAX_COMMENTS = 20
_ISSUE_PATH = re.compile(r"^/(.+)/-/issues/(\d+)/?$")


def parse_ref(text: str) -> tuple[int, str | None, str | None]:
    """`12`, `#12` -> (12, None, None); issue URL -> (12, "group/project", "host")."""
    s = text.strip()
    bare = s[1:] if s.startswith("#") else s
    if bare.isdigit():
        iid, project, host = int(bare), None, None
    else:
        url = urllib.parse.urlparse(s)
        m = (
            _ISSUE_PATH.match(url.path)
            if url.scheme in ("http", "https") and url.hostname
            else None
        )
        if not m:
            raise ValueError("not an issue reference")
        iid, project, host = int(m.group(2)), m.group(1), url.hostname
    if iid <= 0:
        raise ValueError("not an issue reference")
    return iid, project, host


def issue_endpoint(
    iid: int, project: str | None, host: str | None
) -> tuple[list[str], str]:
    path = ":fullpath" if project is None else urllib.parse.quote(project, safe="")
    return (["--hostname", host] if host else []), f"projects/{path}/issues/{iid}"


_ICELANDIC = str.maketrans({"þ": "th", "ð": "d", "æ": "ae", "ö": "o"})


def branch_name(iid: int, title: str) -> str:
    """`<iid>-<first 4 title words>`, lowercase ASCII; e.g. (12, "Röðun verka") -> "12-rodun-verka".

    Team convention (research R5): lowercase, then _ICELANDIC, then NFKD and drop
    non-ASCII, split on runs of non-alphanumerics, keep 4 words. No words -> str(iid).
    """
    # þ/ð/æ don't decompose under NFKD, so map them before it or they'd be dropped.
    ascii_title = unicodedata.normalize("NFKD", title.lower().translate(_ICELANDIC))
    ascii_title = ascii_title.encode("ascii", "ignore").decode()
    words = [w for w in re.split(r"[^a-z0-9]+", ascii_title) if w][:4]
    return "-".join([str(iid), *words])


def compose(issue: dict, notes: list[dict]) -> dict:
    comments = sorted(
        (n for n in notes if not n.get("system")),
        key=lambda n: n["created_at"],
        reverse=True,
    )
    kept, omitted = comments[:MAX_COMMENTS], max(0, len(comments) - MAX_COMMENTS)
    body = (issue.get("description") or "").strip()
    parts = [
        f"GitLab issue #{issue['iid']}: {issue['title']}\nSource: {issue['web_url']}",
        body or "(no description)",
    ]
    if kept:
        parts.append("## Comments (supporting context, newest first)")
        parts += [
            f"@{n['author']['username']} ({n['created_at']}):\n{n['body'].strip()}"
            for n in kept
        ]
    if omitted:
        parts.append(f"({omitted} older comments omitted)")
    return {
        "NUMBER": issue["iid"],
        "TITLE": issue["title"],
        "STATE": issue["state"],
        "URL": issue["web_url"],
        "LABELS": issue.get("labels", []),
        "BRANCH_NAME": branch_name(issue["iid"], issue["title"]),
        "EMPTY_DESCRIPTION": not body,
        "OMITTED_COMMENTS": omitted,
        "DESCRIPTION": "\n\n".join(parts),
    }


def summarize(api_issues: list[dict]) -> dict:
    return {
        "ISSUES": [
            {"NUMBER": i["iid"], "TITLE": i["title"], "LABELS": i.get("labels", [])}
            for i in api_issues
        ]
    }


def view(ref: str) -> None:
    try:
        iid, project, host = parse_ref(ref)
    except ValueError:
        fail(
            2,
            f"not an issue reference: {ref}",
            "Use /speckit-specify directly for plain-text descriptions.",
        )
    hostflags, ep = issue_endpoint(iid, project, host)
    what = f"issue #{iid} not found or not accessible: "
    issue = run_glab([*hostflags, ep], what)
    # ponytail: one page of 100 notes; >100 comments undercounts OMITTED_COMMENTS (research R2).
    notes = run_glab(
        [*hostflags, ep + "/notes?sort=desc&order_by=created_at&per_page=100"], what
    )
    emit(compose(issue, notes))


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        fail(2, message, "Usage: gitlab_issue.py view <ref> | gitlab_issue.py list")


def main(argv: list[str] | None = None) -> None:
    parser = _Parser(prog="gitlab_issue.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("view").add_argument("ref")
    sub.add_parser("list")
    args = parser.parse_args(argv)
    if args.cmd == "view":
        view(args.ref)
    else:
        emit(
            summarize(
                run_glab(
                    [
                        "projects/:fullpath/issues?state=opened&order_by=created_at&sort=desc&per_page=20"
                    ]
                )
            )
        )


if __name__ == "__main__":
    main()
