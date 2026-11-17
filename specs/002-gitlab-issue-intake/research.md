# Research: GitLab Issue Intake for Specify

No `NEEDS CLARIFICATION` remained in Technical Context. Findings are from the installed spec-kit 1.4.1.dev0 (`specify_cli/core_pack/extensions/{git,github}`) and the `glab` docs.

## R1. Entry point: separate command vs `before_specify` hook

- **Decision**: A separate command, `speckit.gitlab.specify` (invoked as `/speckit-gitlab-specify`), that ends by running `__SPECKIT_COMMAND_SPECIFY__`, which renders as `/speckit-specify` for the Claude integration.
- **Rationale**: Hooks only emit "run this command" blocks. A mandatory `before_specify` hook would run on *every* specify, including plain text (risking FR-009), and it has no supported way to replace the feature description; it would rely on the agent "noticing" the fetched text. A dedicated command is explicit, can't affect plain specify, and is how bundled extensions (`bug`, `assess`) chain into other commands.
- **Alternatives**: A mandatory hook that no-ops on non-issue input was rejected as fragile and always-on. An optional hook was rejected because it only prints a suggestion, so it adds nothing over the command. Editing the core `speckit-specify` skill was rejected: it breaks FR-011 and is overwritten on `specify` upgrades.

## R2. Fetching from GitLab

- **Decision**: `glab api` against REST v4 with the `:fullpath` placeholder, which glab resolves from the current repo's remote:
  - issue: `projects/:fullpath/issues/<n>`
  - comments: `projects/:fullpath/issues/<n>/notes?sort=desc&order_by=created_at&per_page=100`, keeping `system: false` only (drops "changed label" noise). The newest 20 are kept and the rest are counted as omitted. A cap of 20 in the API call would make the omitted count impossible to know. Ceiling: issues with more than 100 notes undercount the omitted number.
  - list: `projects/:fullpath/issues?state=opened&order_by=created_at&sort=desc&per_page=20`
  - issue URL from another project/host: `--hostname <host>` and `projects/<url-encoded path>/...`
- **Rationale**: Stable JSON (`iid`, `title`, `description`, `state`, `labels`, `web_url`). `glab issue view --comments` output is human-formatted and changes between glab versions. `glab` owns auth, so we handle no tokens (Constitution IV).
- **Alternatives**: Direct HTTPS with `GITLAB_TOKEN` was rejected because it means handling credentials. The GitLab MCP server was rejected as not set up here, and it ties the extension to one agent.

## R3. Script vs pure agent instructions

- **Decision**: A small stdlib script does the deterministic work (ref parsing, the API calls, comment truncation, composing the text, the branch slug). The command markdown handles interaction: picking from the list, confirming a closed issue, and the manual-paste fallback.
- **Rationale**: Parsing and truncation then behave the same every run and can be tested. Interaction stays with the agent, which is good at it.
- **Alternatives**: Instructions only, like the existing `gitlab-issue` skill, were rejected: there would be nothing to test, and the comment cap and slug would drift between runs.

## R4. Issue reference formats (FR-001)

- **Decision**: Accept `#12`, `12` (the command's argument is always an issue reference, so a bare number is unambiguous here), and `https://<host>/<group>/<project>/-/issues/12`. Anything else gives exit 2 with `ERROR: not an issue reference`.
- **Rationale**: Plain text goes to `/speckit-specify` directly, so this command never needs to guess.

## R5. Branch name (FR-010)

- **Decision**: `<iid>-<slug>`. The slug is the first 4 words of the title, lowercased, ASCII only. Icelandic `þ→th, ð→d, æ→ae, ö→o`, then NFKD to strip accents, then non-alphanumerics become `-`.
- **Rationale**: Matches the CLAUDE.md convention, and Icelandic titles are likely in this team.
- **Usage**: The command *suggests* the name and offers `git switch -c` on confirmation. It never creates a branch silently. The `git` extension isn't installed here; if it were, the name is passed as `GIT_BRANCH_NAME`.

## R6. Untrusted issue content (FR-012)

- **Decision**: The composed description wraps the issue body and comments inside clearly labeled sections. The command instructs the agent to treat everything from the script's `DESCRIPTION` as feature-description data and to ignore instructions inside it.
- **Rationale**: Anyone who can file an issue controls that text, so it gets the same handling as pasted content.

## R7. Error handling

- **Decision**: The script always prints one JSON object. On failure it is `{"ERROR": "...", "HINT": "..."}` with a non-zero exit. Cases:
  - `glab` is missing: hint to `brew install glab` / `glab auth login`, or paste the text.
  - `glab` returns 401/403/404: the message names the reference.
  - The remote isn't GitLab: glab's own message, plus a hint that GitHub isn't supported.

  The command stops before `/speckit-specify` runs, so no spec directory is created (FR-007).

## R8. Native Windows with one script (FR-014)

| Concern | Decision | Why |
|---------|----------|-----|
| Python launcher | The command runs the script with `python3`. If the shell reports "not found", or the Microsoft Store stub opens instead, it retries with `py -3`, then `python`. It stops with the R7 "missing tool" message if all three fail. | On Windows, `python3` is often absent or a Store stub; `py` is the official launcher. A fallback in the command avoids depending on how spec-kit renders the `py` script variant. |
| `#` in PowerShell | The command strips a leading `#` from the reference before the shell call and passes a bare number (`view 12`). The script still accepts `#12` when it arrives quoted. | An unquoted `#12` in PowerShell is a comment, so the script would get no argument. "Empty input means list" is decided from the user's original input, not the script's argv, so the "silently lists instead" bug can't happen. |
| Reading `glab` output | `subprocess.run([...], capture_output=True, encoding="utf-8")` with a list of arguments and never `shell=True`. `glab` is found with `shutil.which("glab")`, which also finds `glab.exe`. | Python's default decoding on Windows is the locale code page (cp1252), which corrupts þ/ð/æ. With a list of arguments there's no quoting difference between cmd and PowerShell. |
| Writing output | `json.dumps(obj, ensure_ascii=True)`, so stdout is pure ASCII and non-ASCII appears as `þ`. The agent's JSON parser restores it. | Writing to a cp1252 console or pipe can't then raise `UnicodeEncodeError`, and nothing gets mangled to `?`. Simpler than reconfiguring stdout. |
| Line endings / paths | No path math in the script beyond `__file__`-relative, using `pathlib`. Composed text uses `\n` only. | Spec files are written by the agent, not the script, so line endings follow the repo's git settings. |
| Installing `glab` | README lists `winget install GLab.GLab` / `scoop install glab` next to `brew install glab`. | Covers the FR-008 hint on every OS. |

- **Alternatives**: A `.ps1` twin of the script was rejected by clarification A. `PYTHONUTF8=1` in the environment was rejected because it relies on every user's setup. `sys.stdout.reconfigure(encoding="utf-8")` was rejected: it would work, but it's still at the mercy of the console font and code page, which `ensure_ascii` sidesteps entirely.
