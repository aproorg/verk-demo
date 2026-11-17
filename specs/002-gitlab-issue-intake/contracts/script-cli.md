# Contract: `gitlab_issue.py`

Location: `extensions/gitlab/scripts/python/gitlab_issue.py`. Stdlib only, Python 3.9+, the same file on Windows, macOS and Linux.

It always writes exactly one JSON object to stdout, **ASCII-only** (`ensure_ascii=True`): non-ASCII characters appear as `\uXXXX` escapes and come back intact when parsed. It reads `glab` output as UTF-8 regardless of the OS locale.

## `view <ref>`

```
python3 gitlab_issue.py view 12          # what the command sends (`#` stripped)
python3 gitlab_issue.py view '#12'       # also accepted when quoted
py -3 gitlab_issue.py view https://gitlab.example.com/acme/verk/-/issues/12   # Windows
```

Success (exit 0):

```json
{
  "NUMBER": 12,
  "TITLE": "Allow marking tasks done",
  "STATE": "opened",
  "URL": "https://gitlab.example.com/acme/verk/-/issues/12",
  "LABELS": ["feature"],
  "BRANCH_NAME": "12-allow-marking-tasks-done",
  "EMPTY_DESCRIPTION": false,
  "OMITTED_COMMENTS": 0,
  "DESCRIPTION": "GitLab issue #12: Allow marking tasks done\nSource: https://...\n\n..."
}
```

`DESCRIPTION` follows the FeatureDescription layout in [data-model.md](../data-model.md).

## `list`

Success (exit 0), at most 20 open issues, newest first:

```json
{ "ISSUES": [ { "NUMBER": 14, "TITLE": "…", "LABELS": ["bug"] } ] }
```

The list is empty when there are no open issues.

## Errors

Non-zero exit with:

```json
{ "ERROR": "issue #99 not found or not accessible", "HINT": "Check the number, or run `glab auth status`." }
```

| Exit | Cause |
|------|-------|
| 2 | not an issue reference / bad usage |
| 3 | `glab` not installed |
| 4 | `glab api` failed: auth, 404, or the remote isn't GitLab. `ERROR` includes glab's stderr |
