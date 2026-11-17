# Quickstart: validate GitLab issue intake

## Prerequisites

- `glab` installed and signed in, then `glab auth login`. Install with:
  - macOS: `brew install glab`
  - Windows: `winget install GLab.GLab` or `scoop install glab`

  It is **not** installed on the planning machine as of 2026-11-17.
- Python 3.9+ (`python3` on macOS/Linux, `py -3` on Windows)
- A checkout whose `origin` is a GitLab project with a few open issues, ideally one whose title has Icelandic characters. This repo's `origin` is GitHub, so use a GitLab sandbox project for the live checks.
- spec-kit ≥ 0.12.17

## 1. Logic check (no GitLab needed)

```bash
python3 extensions/gitlab/scripts/python/test_gitlab_issue.py     # macOS/Linux
py -3 extensions\gitlab\scripts\python\test_gitlab_issue.py       # Windows
```

Expected: `ok`. Covers:
- ref parsing, including bare `12` and quoted `#12` (FR-001)
- slug/branch name with Icelandic characters (FR-010)
- description composition with comments and the omitted count
- empty-description handling
- ASCII-only JSON output that round-trips þ/ð/æ/ö (FR-014)

## 2. Install / remove (FR-011)

```bash
specify extension add --dev extensions/gitlab
specify extension list            # shows gitlab
specify extension remove gitlab   # skill is gone, core files untouched
```

Check that `.claude/skills/speckit-gitlab-specify/` appears after `add` and is gone after `remove`.

## 3. Live scenarios (in a GitLab checkout)

| # | Do | Expect |
|---|----|--------|
| 1 | `/speckit-gitlab-specify #<open>` | Spec created. Its Input line names the issue and URL. Branch `<n>-…` suggested |
| 2 | Same with the issue URL | Same result |
| 3 | `/speckit-gitlab-specify` | Up to 20 open issues listed. Picking one continues as in #1 |
| 4 | `/speckit-gitlab-specify #<closed>` | Warning, then it waits for confirmation |
| 5 | `/speckit-gitlab-specify #999999` | Error naming #999999. `specs/` is unchanged |
| 6 | Make `glab` unavailable (macOS: `PATH=/usr/bin:/bin`; Windows: rename `glab.exe` temporarily), then run #1 | "glab not installed" + manual paste offered |
| 7 | `/speckit-specify some plain text` | Same as before installing (FR-009) |
| 8 | Issue whose body says "ignore the template and …" | Spec still follows the template (FR-012) |

## 4. Windows run (SC-006, required before merge)

On a Windows machine, in **PowerShell**:

1. Run step 1 with `py -3` and expect `ok`.
2. Run step 2.
3. Run all of section 3.
4. Also check:

| # | Do | Expect |
|---|----|--------|
| W1 | `/speckit-gitlab-specify #<open>` | Shows issue `<open>`, **not** the open-issue list (the `#` was not eaten) |
| W2 | Issue with þ/ð/æ/ö in the title or a comment | Characters are intact in `spec.md`; branch slug uses `th/d/ae/o` |
| W3 | Machine where `python3` is missing or opens the Store | Command falls back to `py -3` and succeeds |

Record the result (pass/fail per row, Windows and PowerShell version) in the merge request description.
