# Implementation Plan: GitLab Issue Intake for Specify

**Branch**: `<issue-number>-gitlab-issue-intake` (not created; no issue yet) | **Date**: 2026-11-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-gitlab-issue-intake/spec.md`

## Summary

Add a project-local spec-kit extension, `gitlab`, that provides one command, `/speckit-gitlab-specify`. Given an issue reference, or nothing (which means "list open issues"), it calls a small stdlib Python script that fetches the issue with `glab api` and returns JSON: the composed feature description, state, the suggested branch name and how many comments were omitted. The command then runs `/speckit-specify` with that description. Core `/speckit-specify` is not modified and no hook is registered, so plain-text specify is unchanged (FR-009, FR-011). See [research.md](./research.md) for why this is a separate command and not a `before_specify` hook.

The same single script runs on native Windows, macOS and Linux (FR-014, clarified 2026-11-17). Windows needs four things, all in research R8:
- the command falls back between Python launchers
- it strips `#` before calling the script
- the script reads `glab` output explicitly as UTF-8
- its JSON output is ASCII-only

## Technical Context

**Language/Version**: Python 3.9+ standard library only. 3.9 rather than 3.11 because Windows machines often have an older Python, and nothing here needs newer.

**Primary Dependencies**: `glab` CLI (external tool, already assumed by the `gitlab-issue` skill), spec-kit ≥ 0.12.17 extension mechanism

**Storage**: N/A (read-only, nothing persisted besides the spec that `/speckit-specify` writes)

**Testing**: one plain-assert test file runnable with `python3` or `py -3` (no pytest needed). `glab` is mocked by feeding JSON fixtures to pure functions. Windows is verified by one manual run of the test plus the quickstart live checks, recorded in the MR. No CI is added (spec clarification).

**Target Platform**: developer machines running Claude Code with spec-kit: native Windows (PowerShell, cmd), macOS, Linux

**Project Type**: developer tooling: a spec-kit extension (command markdown + script)

**Performance Goals**: one issue fetch = 2 `glab api` calls (issue + notes); list = 1 call

**Constraints**: read-only toward GitLab (FR-013); issue text is untrusted data (FR-012); no new Python packages (Constitution IV); no shell-specific syntax in the script or its invocation, so one code path serves every OS (FR-014)

**Scale/Scope**: 1 manifest, 1 command, 1 script (~150 lines), 1 test file, 1 README

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|-----------|--------|------|
| I. Layering (API/web) | N/A | Touches neither `api/` nor `web/`. |
| II. Tests follow behavior | PASS (adapted) | The pytest-on-service-and-endpoint rule targets the API. Here the script's pure logic gets a runnable test: ref parsing, slug, compose, truncation, and the Windows cases (`#`, non-ASCII round-trip). `task check` stays green because nothing in it changes. |
| III. One API/web contract | N/A | No API model changes. |
| IV. Simplicity, no new packages/auth/DB | PASS | Stdlib only. `glab` is an external CLI the team already uses, not a project dependency. No credentials handled by us; `glab` owns auth. |
| V. Bounded scope | PASS | No changes to core speckit files, `api/`, `web/` or `Taskfile.yml`. No CI added. GitHub support is excluded and would need its own issue. |
| Language: code English, UI Icelandic | PASS | Code/identifiers English. Messages are developer-facing CLI output (English, matching speckit). |
| No real data | PASS | Test fixtures use made-up issues/names. |
| Branch `<issue>-<desc>`, never commit to main | ACTION | An issue must be created before implementing (`/create-issue`), then a branch with that number. |

**Post-design re-check**: still PASS. The design adds no hook, so core flows are untouched.

## Project Structure

### Documentation (this feature)

```text
specs/002-gitlab-issue-intake/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── command.md        # /speckit-gitlab-specify behavior
│   └── script-cli.md     # gitlab_issue.py input/output JSON
└── tasks.md              # /speckit-tasks (not yet)
```

### Source Code (repository root)

```text
extensions/gitlab/
├── extension.yml                         # manifest: id gitlab, 1 command, requires glab
├── README.md                             # install / usage / limits
├── commands/
│   └── speckit.gitlab.specify.md         # agent instructions; ends by running /speckit-specify
└── scripts/python/
    ├── gitlab_issue.py                   # `view <ref>` and `list` -> JSON on stdout
    └── test_gitlab_issue.py              # plain asserts, `python3 test_gitlab_issue.py`
```

Installed into this project with `specify extension add --dev extensions/gitlab`, which registers the `speckit-gitlab-specify` skill under `.claude/skills/`.

**Structure Decision**: The source sits in the repo under `extensions/gitlab/`, mirroring the layout of the bundled `github` extension, so it can be reviewed, versioned and later published to a catalog unchanged.

## Complexity Tracking

No violations. Deliberately skipped:

- **`before_specify` hook**: hooks can't rewrite the specify input; see research R1.
- **bash/PowerShell script variants**: Windows runs the same Python script (clarification A), so a `.ps1` twin would only duplicate behavior. Add one only if a Python-less Windows setup has to be supported.
- **GitHub support**: out of scope per spec.
