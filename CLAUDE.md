# verk-demo

Full-stack sýnidæmi: verk og eigendur. `api/` er FastAPI, `web/` er Vite + React + TypeScript.

## Skipanir
Allar skipanir eru í `Taskfile.yml` og keyra úr rótinni.
- Allt grænt?: `task check` (test, lint, build)
- Prófa API:   `task test` (eitt próf: `task test -- -k <nafn>`)
- Lint, snið:  `task lint`, `task format`
- Athuga vef:  `task build` (tsc + vite build)
- Keyra:       `task dev` (API á :8000, vefur á :3000)

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
