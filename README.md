# verk-demo

Lítið full-stack sýnidæmi fyrir námskeið í Claude Code: verk og eigendur.

- `api/` · FastAPI, gögn geymd í minni, pytest
- `web/` · Vite + React + TypeScript

Öll gögn eru gervigögn.

## Skipanir

Allt keyrir í gegnum [Task](https://taskfile.dev) úr rót verkefnisins. `task` eitt og sér sýnir listann.

```sh
task install     # uv sync og npm install
task dev         # API á :8000 og vefur á :3000, saman
task test        # pytest. Viðföng á eftir --: task test -- -k complete
task lint        # ruff check
task format      # ruff format
task build       # tsc + vite build
task check       # test, lint og build: allt sem þarf að vera grænt fyrir commit
```

`task api` og `task web` keyra hvort fyrir sig. Vite sendir `/tasks` og `/owners` áfram á API-ið.

Þarf: [uv](https://docs.astral.sh/uv/), Node 20.19+ og Task (`winget install Task.Task`, `brew install go-task`).
Án Task: skipanirnar standa í `Taskfile.yml`.

## Claude Code

Allt er sett upp á `main`: `CLAUDE.md` og `.claude/` með reglum, skills, subagentum, hooks, MCP og workflow.
Sjá [CLAUDE-FEATURES.md](CLAUDE-FEATURES.md) fyrir yfirlit og eina sýnikennslu á hverja einingu.

Uppsetningin er líka plugin. Í öðru repoi:

```text
/plugin marketplace add aproorg/verk-demo
/plugin install verk-dev@verk-demo
```
