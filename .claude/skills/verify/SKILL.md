---
name: verify
description: Keyrir öll próf og athuganir í api/ og web/ og dregur niðurstöðuna saman. Notað áður en breyting er commituð eða þegar spurt er hvort allt sé grænt.
allowed-tools: Bash(uv run pytest *) Bash(uv run ruff *) Bash(npm run build*)
---

Staðan núna:

- Grein: !`git branch --show-current`
- Breyttar skrár: !`git status --short`

Keyrðu í þessari röð og stoppaðu ekki við fyrstu villu:

1. `cd api && uv run pytest -q`
2. `cd api && uv run ruff check .`
3. `cd web && npm run build`

Skilaðu einni töflu: athugun, staða (✓ eða ✗), og fyrsta villulína ef einhver er.
Lagaðu ekkert nema beðið sé um það.
