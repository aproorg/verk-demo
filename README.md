# verk-demo

Lítið full-stack sýnidæmi fyrir námskeið í Claude Code: verk og eigendur.

- `api/` · FastAPI, gögn geymd í minni, pytest
- `web/` · Vite + React + TypeScript

Öll gögn eru gervigögn.

## Keyra

Tveir gluggar:

```sh
cd api
uv run fastapi dev app/main.py      # http://localhost:8000/docs
```

```sh
cd web
npm install
npm run dev                         # http://localhost:5173
```

Vite sendir `/tasks` og `/owners` áfram á API-ið á porti 8000.

## Prófa

```sh
cd api && uv run pytest
cd api && uv run ruff check .
cd web && npm run build             # tsc + vite build
```

## Claude Code

Allt er sett upp á `main`: `CLAUDE.md` og `.claude/` með reglum, skills, subagentum, hooks, MCP og workflow.
Sjá [CLAUDE-FEATURES.md](CLAUDE-FEATURES.md) fyrir yfirlit og eina sýnikennslu á hverja einingu.
