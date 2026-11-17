# Data Model: GitLab Issue Intake for Specify

Nothing is persisted. These are the in-flight shapes passed between `glab`, the script and the command.

## IssueRef (parsed from the command argument)

| Field | Type | Rule |
|-------|------|------|
| iid | int > 0 | From `#12`, `12`, or `/-/issues/12` |
| project | str \| None | URL path (`group/sub/project`), else `None` = current repo (`:fullpath`) |
| host | str \| None | URL host, else `None` = glab default |

Invalid input → `ERROR: not an issue reference`.

## FetchedIssue (from GitLab REST v4)

| Field | Source | Notes |
|-------|--------|-------|
| iid | `iid` | Project-scoped number shown as `#n` |
| title | `title` | |
| description | `description` | May be `null`/empty → warning |
| state | `state` | `opened` \| `closed` |
| labels | `labels` | list of str |
| url | `web_url` | |
| comments | `/notes`, `system == false` | newest 20; each: author `username`, `created_at`, `body` |

## FeatureDescription (script output → `/speckit-specify` input)

Composed text, in this order:

1. `GitLab issue #<iid>: <title>`
2. `Source: <url>`
3. Description body (or `(no description)`)
4. `## Comments (supporting context, newest first)`: one block per comment, `@<author> (<date>):` + body. Omitted entirely when there are none.
5. If truncated: `(<k> older comments omitted)`

## State rules

- `state == closed` → the command must get explicit confirmation before continuing (FR-006).
- `description` empty → continue with title only, and warn (spec edge case).
