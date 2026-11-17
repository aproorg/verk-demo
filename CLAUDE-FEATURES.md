# Claude Code í þessu repoi

Þetta er sett upp á `main`. Hver lína er eitthvað sem hægt er að sýna. Greinin `start` er appið án alls þessa.

| Eining | Skrá | Prófaðu |
|---|---|---|
| Minni verkefnisins | `CLAUDE.md` | `/memory`, `/context` |
| Reglur eftir slóð | `.claude/rules/api.md`, `web.md` | Biddu Claude að opna `web/src/App.tsx` og svo `/context`: vef-reglan hleðst inn, API-reglan ekki |
| Skill með viðföngum | `.claude/skills/gitlab-issue/` | `/gitlab-issue 1` |
| Skill með skeljarinnskoti og leyfðum tólum | `.claude/skills/verify/` | `/verify` |
| Subagent á ódýrara líkani | `.claude/agents/issue-implementer.md` | „Notaðu issue-implementer á issue 1“ |
| Subagent sem má bara lesa | `.claude/agents/code-reviewer.md` | „Láttu code-reviewer rýna greinina“, `/agents` |
| Heimildir | `.claude/settings.json` → `permissions` | `/permissions`. Próf keyra án þess að spurt sé, `.env` er aldrei lesið |
| Hook fyrir tólakall | `.claude/hooks/protect_main.py` | Biddu Claude að commita á `main`: kallinu er hafnað |
| Hook eftir tólakall | `.claude/hooks/format_python.py` | Hver `.py`-skrá sem Claude breytir er sniðin með ruff |
| MCP | `.mcp.json` | `/mcp`. Playwright: „Opnaðu localhost:5173 og bættu við verki“ |
| Workflow | `.claude/workflows/review-branch.js` | `/review-branch`, fylgstu með í `/workflows` |
| Úttaksstíll | `.claude/output-styles/kennari.md` | `/output-style Kennari` |

## Bætist við á námskeiðinu

- **Spec Kit:** `git switch -c speckit` og `specify init --here --force --integration claude`. Bætir við `.specify/` og `.claude/skills/speckit-*`.
- **Marketplace:** skills og agentar héðan eru afritaðir í `plugins/<nafn>/` í sér repoi í GitLab og settir upp með `/plugin`.

## Gott að vita

- Hooks keyra með `uv run`, þannig að þeir virka eins á Windows, macOS og Linux.
- MCP-þjónninn í `.mcp.json` þarf samþykki í fyrstu lotu og sækir pakka með `npx`.
- Workflows þurfa að vera virk á aðganginum (`/config` á Pro).
- Það sem er bara fyrir þig fer í `CLAUDE.local.md` og `.claude/settings.local.json`. Hvorugt fer í git.
