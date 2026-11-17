# GitLab Issue Intake

Spec-kit extension that turns a GitLab issue into the input for `/speckit-specify`, so you don't copy issue text by hand and the spec links back to its issue.

## Install / remove

```bash
specify extension add --dev extensions/gitlab
specify extension remove gitlab
```

## Usage

```text
/speckit-gitlab-specify 12
/speckit-gitlab-specify #12
/speckit-gitlab-specify https://gitlab.example.com/acme/verk/-/issues/12
/speckit-gitlab-specify            # list open issues and pick one
```

The command fetches the issue and its comments, warns on a closed issue or an empty description, suggests the branch `<iid>-<slug>` (e.g. `12-rodun-verka`), and then runs `/speckit-specify`. For plain text, use `/speckit-specify` directly.

## Prerequisites

| | macOS / Linux | Windows |
|---|---|---|
| glab | `brew install glab` | `winget install GLab.GLab` or `scoop install glab` |
| Sign in | `glab auth login` | `glab auth login` |
| Python 3.9+ | `python3` | `py -3` |

Logic test, no GitLab needed: `python3 extensions/gitlab/scripts/python/test_gitlab_issue.py` should print `ok`.

## Limits

- GitLab only, not GitHub. The project comes from the current repo's remote, unless you pass an issue URL.
- Uses the newest 20 comments and says how many were left out. Undercounts on issues with more than 100 comments.
- Lists at most 20 open issues, newest first.
- Read-only: never writes to GitLab.
- Attachments and images are not downloaded; only their links stay in the text.
