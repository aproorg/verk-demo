---
name: report-bug
description: Stofnar stutt bug-issue fyrir villu sem fannst á meðan unnið var að öðru verkefni og heldur svo áfram með verkefnið. Notað þegar þú rekst á villu, brotna hegðun eða galla sem verkefnið/issue-ið nefnir ekki, t.d. við prófun í vafra, lestur kóða eða keyrslu prófa.
---

Villa utan sviðs: lagaðu hana ekki (CLAUDE.md: „Ekki breyta því sem issue-ið nefnir ekki"). Skráðu hana og haltu áfram. Ekki stoppa til að spyrja; notandinn hefur samþykkt að slík issue séu stofnuð.

1. Staðfestu að þetta sé villa en ekki afleiðing af þinni eigin breytingu. Ef breytingin þín olli henni er hún innan sviðs: lagaðu hana.
2. Leitaðu að tvítekningu: `gh issue list --state open --search "<lykilorð>"`. Ef til er issue: bættu við athugasemd aðeins ef þú hefur nýjar upplýsingar, annars sleppa.
3. Stofnaðu issue-ið á ensku, stutt:

   ```sh
   gh issue create --label bug --title "<what is broken, where>" --body "<texti>"
   ```

   Body:
   - **What happens** og **expected**, eitt til tvö orð hvort ef hægt er.
   - **Repro:** lágmarksskref (skipun, slóð, gluggastærð, inntak).
   - **Where:** `skrá:lína` ef þekkt.
   - **Found while:** greinin/issue-ið sem verið var að vinna í, t.d. „while working on #6".
   - Engin raungögn og engin skjáskot með persónuupplýsingum.

   Ef `origin` er á GitLab: `glab issue create --label bug --title ... --description ...`. Ef hvorugt tólið virkar: skrifaðu textann í lokaskýrsluna í staðinn.
4. Haltu áfram með upprunalega verkefnið. Nefndu issue-númerið í lokaskýrslunni til notandans og í PR-lýsingunni undir „Found along the way", ekki sem `Closes`.

Dæmi: við vafraprófun á froskum (#6) flæddi „Bæta við"-formið út fyrir skjáinn á 320 px. Það tengdist ekki froskunum, svo það var bug-issue, ekki breyting á greininni.
