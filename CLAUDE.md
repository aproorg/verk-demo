# verk-demo

Full-stack sýnidæmi: verk og eigendur. `api/` er FastAPI, `web/` er Vite + React + TypeScript.

## Skipanir
- Prófa API:   `cd api && uv run pytest`
- Lint API:    `cd api && uv run ruff check .`
- Athuga vef:  `cd web && npm run build` (tsc + vite build)
- Keyra:       `cd api && uv run fastapi dev app/main.py` og `cd web && npm run dev`

## Arkitektúr
- `api/app/main.py` endapunktar, `services.py` viðskiptalógík, `models.py` Pydantic-líkön
- Gögn eru geymd í minni í `TaskService`. Það er viljandi
- `web/src/api.ts` er eini staðurinn sem kallar á API-ið. Týpurnar þar spegla `models.py`

## Venjur
- Kóði, commit og auðkenni á ensku. Texti í viðmóti á íslensku
- Ný hegðun fær pytest-próf, bæði á þjónustu og endapunkt
- Breyting á API-líkani kallar á sömu breytingu í `web/src/api.ts`
- Greinar heita `<issue-númer>-<stutt-lýsing>`

## Ekki
- Ekki bæta við auðkenningu, gagnagrunni eða nýjum pökkum án þess að spyrja
- Ekki breyta því sem issue-ið nefnir ekki
- Ekki commita á `main`
- Engin raungögn: aðeins gervinöfn og gervigögn
