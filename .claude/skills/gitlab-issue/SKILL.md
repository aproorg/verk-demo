---
name: gitlab-issue
description: Útfærir GitLab issue frá áætlun að merge request. Notað þegar unnið er eftir issue-númeri eða slóð.
argument-hint: "[issue-númer eða slóð]"
---

Útfærðu GitLab issue $ARGUMENTS.

1. Sæktu issue-ið með `glab issue view $ARGUMENTS --comments`.
   Ef glab er ekki uppsett eða innskráð: biddu notandann að líma textann inn.
2. Dragðu saman samþykktarskilyrðin. Ef hegðun er óljós: spurðu, ekki giska.
3. Búðu til grein sem heitir `<númer>-<stutt-lýsing>`.
4. Leggðu fram áætlun og bíddu eftir samþykki.
5. Útfærðu í stíl verkefnisins (sjá CLAUDE.md) og skrifaðu próf.
6. Keyrðu prófin og lagaðu þar til þau standast.
7. Sýndu diff-ið. Ekki commita og ekki opna merge request án samþykkis.
8. Eftir samþykki: commit, `git push -u origin <grein>` og
   `glab mr create --draft --title "<titill>" --description "Closes #<númer>" --yes`.
