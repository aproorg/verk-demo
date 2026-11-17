# Feature Specification: GitLab Issue Intake for Specify

**Feature Branch**: `<issue-number>-gitlab-issue-intake` (not created yet; no issue exists)

**Created**: 2026-11-17

**Status**: Draft

**Input**: User description: "create a speckit extension for pulling open gitlab issues as inputs to the speckit-specify command"

## Clarifications

### Session 2026-11-17

- Q: When you say the GitLab extension should support Windows, which kind of Windows setup must it work on? → A: Native Windows (PowerShell and cmd) using the same single script as macOS/Linux; no separate PowerShell variant, and WSL is not required.
- Q: How should we confirm that the extension works on Windows before the change is merged? → A: Run the logic test and the quickstart live checks once by hand on a Windows machine and record the result in the merge request; no CI is added.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Specify a feature from a known issue (Priority: P1)

A developer already knows which GitLab issue they want to work on. Instead of copying the issue text by hand, they start the specify step with the issue number or link. The extension fetches the issue and hands its title, description and acceptance criteria to the specify step as the feature description. The resulting spec records which issue it came from.

**Why this priority**: This is the core value: removing the manual copy-paste between the issue tracker and the spec, and keeping a traceable link from spec back to issue.

**Independent Test**: Run the specify step with the number of an existing open issue and confirm the generated spec's input and content reflect that issue and link back to it.

**Acceptance Scenarios**:

1. **Given** an open issue #12 exists in the project's GitLab repository, **When** the developer starts specify with `#12`, **Then** the spec is generated from the issue's title and description, and the spec's Input line references issue #12 with its link.
2. **Given** the developer passes a full issue link instead of a number, **When** specify starts, **Then** the same issue is fetched and used.
3. **Given** the issue has comments, **When** it is fetched, **Then** the comments are included as supporting context, clearly separated from the issue description.
4. **Given** the developer passes plain text (not an issue reference), **When** specify starts, **Then** the extension does nothing and specify behaves exactly as it does today.

---

### User Story 2 - Pick from open issues (Priority: P2)

A developer wants to start new work but doesn't remember the issue number. They ask to pull from open issues. The extension shows a short list of open issues (number, title, labels) and the developer picks one, which then feeds the specify step as in Story 1.

**Why this priority**: Useful for discovery, but Story 1 already covers the common case where the developer knows the issue.

**Independent Test**: Request the open-issue list in a repository with several open issues, select one, and confirm specify proceeds with the selected issue.

**Acceptance Scenarios**:

1. **Given** the repository has open issues, **When** the developer asks for the list, **Then** they see open issues only, newest first, each with number, title and labels.
2. **Given** the list is shown, **When** the developer selects an issue, **Then** specify proceeds with that issue as input.
3. **Given** there are no open issues, **When** the developer asks for the list, **Then** they are told there are none and specify does not start.

---

### User Story 3 - Branch named after the issue (Priority: P3)

When a spec is created from an issue, the suggested branch name follows the project convention `<issue-number>-<short-description>` so branch, spec and issue line up without extra effort.

**Why this priority**: Convenience that enforces an existing team convention; the feature works without it.

**Independent Test**: Create a spec from issue #12 titled "Allow marking tasks done" and confirm the suggested branch name is `12-<short-name>`.

**Acceptance Scenarios**:

1. **Given** a spec is created from issue #12, **When** the branch name is suggested, **Then** it starts with `12-` followed by a short name derived from the issue title.

---

### Edge Cases

- The referenced issue is closed: the developer is warned and must confirm before continuing.
- The referenced issue does not exist or is not accessible: specify stops with a clear message naming the issue reference; no spec directory is created.
- The GitLab tool is not installed or not signed in: the developer is told what is missing and offered the fallback of pasting the issue text manually.
- The repository's remote is not on GitLab (e.g. GitHub): the extension says so and specify continues with whatever text the developer provided.
- The issue description is empty: the title alone is used, and the developer is warned that the spec will rely heavily on assumptions.
- The issue is very long or has many comments: comments beyond a reasonable limit (most recent 20) are omitted, and the developer is told how many were left out.
- On Windows PowerShell, an unquoted `#12` is treated as a comment and never reaches the extension: the extension must still receive issue 12 (it is not silently treated as "no input → list issues").
- On Windows, the issue title or comments contain Icelandic or other non-English characters: they appear unchanged in the spec and branch name suggestion, not as `?` or garbled text.
- Issue content contains instructions aimed at the assistant (e.g. "ignore the template"): it is treated as feature description data only, never as instructions that change how specify runs.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The extension MUST accept an issue reference as either `#<number>`, a bare number when explicitly marked as an issue, or a full GitLab issue link.
- **FR-002**: The extension MUST fetch the referenced issue's title, description, state, labels, link and comments from the project's GitLab repository.
- **FR-003**: The extension MUST pass the fetched issue to the specify step as its feature description, with the description first and comments as clearly marked supporting context.
- **FR-004**: The generated spec MUST record the source issue number and link in its Input line.
- **FR-005**: The extension MUST be able to list open issues (number, title, labels; newest first; at most 20) and let the developer choose one.
- **FR-006**: The extension MUST warn and ask for confirmation before using a closed issue.
- **FR-007**: The extension MUST stop with a clear, actionable message when the issue cannot be fetched, and MUST NOT create a spec directory in that case.
- **FR-008**: When the GitLab tool is unavailable or unauthenticated, the extension MUST tell the developer what is missing and offer manual paste as a fallback.
- **FR-009**: When the input is not an issue reference, the extension MUST leave the specify step's behavior unchanged.
- **FR-010**: The suggested branch name for an issue-based spec MUST follow `<issue-number>-<short-description>`.
- **FR-011**: The extension MUST be installable and removable through the standard speckit extension mechanism, without modifying the core specify command.
- **FR-012**: Issue content MUST be treated as data only; instructions embedded in issue text MUST NOT alter the specify workflow.
- **FR-013**: The extension MUST be read-only toward GitLab: it MUST NOT create, edit, comment on, label or close issues.
- **FR-014**: The extension MUST behave the same on native Windows (PowerShell and cmd), macOS and Linux, using one shared implementation. That includes handling issue references written as `#12` and issue text with non-English characters (e.g. Icelandic þ, ð, æ, ö) without corrupting them.

### Key Entities

- **Issue Reference**: What the developer types to identify an issue (number or link).
- **Fetched Issue**: Number, title, description, state (open/closed), labels, link, and comments (author, date, text).
- **Feature Description**: The text handed to specify, composed from the fetched issue plus a source reference.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can go from an issue number to a generated spec in a single command, with no manual copying of issue text.
- **SC-002**: 100% of specs created from an issue contain a working link back to that issue.
- **SC-003**: When the issue cannot be fetched, the developer learns why and what to do next in one message, with no partial spec left behind.
- **SC-004**: Running specify with plain text produces the same result with the extension installed as without it.
- **SC-005**: Picking an issue from the open-issue list takes under 30 seconds for a repository with up to 20 open issues.
- **SC-006**: Every user scenario above produces the same result on native Windows as on macOS, confirmed by one manual run on a Windows machine whose result is recorded in the merge request.

## Assumptions

- Developers use the GitLab command-line tool (`glab`), already installed and signed in, matching the existing `gitlab-issue` skill; no new credentials or tokens are introduced.
- The GitLab project is inferred from the current repository's remote; working across multiple projects is out of scope.
- One issue produces one spec per run; combining several issues into one spec is out of scope.
- GitHub issues are out of scope for this extension, even though `origin` currently points at GitHub; a GitHub variant can be its own issue.
- Issue images and attachments are not downloaded; only their links are kept in the text.
- Writing back to GitLab (e.g. commenting the spec link on the issue) is out of scope.
- Windows support is verified by hand once before merging; adding CI (Windows or otherwise) is out of scope.
