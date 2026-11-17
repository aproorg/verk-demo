# verk-demo Constitution

## Core Principles

### I. Skýr lagskipting

- Endapunktar í `api/app/main.py` MUST vera þunnir: þeir kalla á `TaskService` og þýða
  niðurstöðuna í HTTP-svar.
- Viðskiptalógík MUST búa í `services.py`. Þjónustan kastar eigin undantekningum og aðeins
  `main.py` má þekkja `HTTPException`.
- Skilatýpur endapunkta MUST vera Pydantic-líkön úr `models.py`, ekki `dict`.
- Á vefnum MUST öll `fetch`-köll fara í gegnum `request()` í `web/src/api.ts`.

Rök: Þegar hvert lag hefur eitt hlutverk er hægt að prófa lógík án HTTP og breyta
flutningslaginu án þess að snerta lógíkina.

### II. Próf fylgja hegðun (NON-NEGOTIABLE)

- Ný eða breytt hegðun MUST fá pytest-próf, bæði á þjónustu og á endapunkt.
- Próf MUST nota `client`- og `service`-fixture og MUST NOT reiða sig á gögnin úr
  `seeded_service()`.
- Breyting telst ekki lokið fyrr en `task check` (test, lint, build) er grænt.

Rök: Próf á báðum lögum grípa bæði villur í lógík og villur í þýðingu yfir í HTTP.

### III. Einn samningur milli API og vefs

- Týpurnar í `web/src/api.ts` MUST spegla `api/app/models.py`. Breyting á API-líkani MUST
  fylgja sama breyting í `api.ts` í sömu grein.
- Aðgerð sem breytir stöðu á tilfangi sem er til MUST vera `PATCH /<tilföng>/{id}/<sögn>`
  án body og skila uppfærða tilfanginu með `200`.

Rök: Samningurinn er skrifaður á tveimur stöðum. Hann helst aðeins réttur ef báðir staðir
breytast saman.

### IV. Einfaldleiki fram yfir innviði

- Gögn eru geymd í minni í `TaskService`. Það er viljandi og MUST NOT breytast án samþykkis.
- Auðkenning, gagnagrunnur og nýir pakkar MUST NOT bætast við án þess að spyrja fyrst.
- Vefurinn MUST nota function components og hooks. Ekkert state-safn og ekkert UI-safn.

Rök: Þetta er sýnidæmi. Hver innviður sem bætist við dregur athyglina frá því sem dæmið
á að sýna.

### V. Afmarkað umfang

- Breyting MUST NOT snerta það sem issue-ið nefnir ekki.
- Viðbót sem fer út fyrir issue-ið MUST fá eigið issue.

Rök: Litlar og afmarkaðar breytingar er hægt að rýna og bakka með.

## Skorður

- **Tækni**: `api/` er FastAPI og Pydantic, `web/` er Vite, React og TypeScript. Allar
  skipanir eru í `Taskfile.yml` og keyra úr rótinni.
- **Tungumál**: Kóði, commit og auðkenni MUST vera á ensku. Texti sem notandi sér MUST vera
  á íslensku.
- **Gögn**: Engin raungögn. Aðeins gervinöfn og gervigögn, í kóða, prófum og skjölum.
- **Aðgengi**: Innsláttarsvið MUST hafa `aria-label`. Villur MUST birtast í `role="alert"`,
  ekki í `console.log`.

## Verkflæði og gæðahlið

- Öll vinna fer fram á grein sem heitir `<issue-númer>-<stutt-lýsing>`. MUST NOT commita
  á `main`.
- `task check` MUST vera grænt áður en merge request er opnað.
- Rýni á merge request MUST staðfesta að breytingin fylgi meginreglunum hér að ofan.

## Governance

- Þessi stjórnarskrá gengur framar öðrum venjum í verkefninu. `CLAUDE.md` og
  `.claude/rules/` lýsa daglegri framkvæmd og MUST vera í samræmi við hana.
- Breyting á stjórnarskránni fer í gegnum merge request sem lýsir breytingunni og rökum
  hennar og uppfærir `CLAUDE.md` og reglurnar ef þær stangast á við hana.
- Útgáfunúmer fylgir semantic versioning: MAJOR þegar meginregla er fjarlægð eða
  endurskilgreind, MINOR þegar meginregla eða kafli bætist við, PATCH fyrir orðalag og
  skýringar.
- Frávik frá meginreglu MUST vera rökstutt í merge request. Órökstutt frávik stöðvar
  samþykkt.

**Version**: 1.0.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-17
