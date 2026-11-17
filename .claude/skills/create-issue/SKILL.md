---
name: create-issue
description: Rannsakar kóðann út frá stuttri lýsingu, skrifar ítarlegt issue (hegðun, útfærsla, samþykktarskilyrði, utan sviðs) og stofnar það í GitLab eða GitHub eftir samþykki.
argument-hint: "[stutt lýsing á verkinu]"
disable-model-invocation: true
---

Búðu til issue úr þessari lýsingu: $ARGUMENTS

Remote verkefnisins:

!`git remote -v`

1. Rannsakaðu kóðann áður en þú skrifar. Finndu endapunkta, þjónustuaðferðir, líkön, próf og vefhluta sem verkið snertir, og hvernig sambærileg hegðun er útfærð í dag. Lestu `CLAUDE.md` og `.claude/rules/` til að fylgja venjum verkefnisins.
2. Skrifaðu issue-ið á ensku, nógu ítarlegt til að hægt sé að útfæra það án frekari spurninga:
   - **Titill:** stuttur, í boðhætti.
   - **Hegðun:** hvað á að gerast, séð frá notandanum.
   - **Útfærsla:** hvað breytist í hverju lagi, með réttum skráarheitum og auðkennum úr kóðanum: endapunktur (aðferð, slóð, stöðukóðar), líkön, þjónusta, vefur og próf.
   - **Samþykktarskilyrði:** listi af atriðum sem hægt er að prófa, villutilvik meðtalin.
   - **Utan sviðs:** hvað á að láta í friði.
3. Tæknilegar ákvarðanir sem kóðinn svarar tekur þú sjálfur og skráir í issue-ið. Spurðu aðeins um það sem hvorki lýsingin né kóðinn svarar, t.d. hvaða hegðun notandinn vill. Ekki giska á það.
4. Sýndu issue-ið og bíddu eftir samþykki. Ekki stofna neitt fyrr.
5. Eftir samþykki, eftir því hvar `origin` er:
   - GitLab: `glab issue create --title "<titill>" --description "<texti>"`
   - GitHub: `gh issue create --title "<titill>" --body "<texti>"`
   Ef hvorugt tólið er uppsett eða innskráð: skilaðu textanum svo hægt sé að líma hann inn.
6. Skilaðu númeri og slóð á issue-ið.
