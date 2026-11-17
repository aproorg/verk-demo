---
name: create-issue
description: Skrifar vel afmarkað issue (hegðun, samþykktarskilyrði, utan sviðs) úr stuttri lýsingu og stofnar það í GitLab eða GitHub eftir samþykki.
argument-hint: "[stutt lýsing á verkinu]"
disable-model-invocation: true
---

Búðu til issue úr þessari lýsingu: $ARGUMENTS

Remote verkefnisins:

!`git remote -v`

1. Lestu kóðann sem lýsingin snertir, nóg til að nefna rétta endapunkta, skrár og heiti.
2. Skrifaðu issue-ið á ensku með þessari uppbyggingu:
   - **Titill:** stuttur, í boðhætti.
   - **Hegðun:** ein til tvær setningar um hvað á að gerast.
   - **Samþykktarskilyrði:** listi af atriðum sem hægt er að prófa.
   - **Utan sviðs:** hvað á að láta í friði.
3. Ef lýsingin dugar ekki til að skrifa samþykktarskilyrði: spurðu, ekki giska.
4. Sýndu issue-ið og bíddu eftir samþykki. Ekki stofna neitt fyrr.
5. Eftir samþykki, eftir því hvar `origin` er:
   - GitLab: `glab issue create --title "<titill>" --description "<texti>"`
   - GitHub: `gh issue create --title "<titill>" --body "<texti>"`
   Ef hvorugt tólið er uppsett eða innskráð: skilaðu textanum svo hægt sé að líma hann inn.
6. Skilaðu númeri og slóð á issue-ið.
