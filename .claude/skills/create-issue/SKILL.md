---
name: create-issue
description: Rannsakar kóðann út frá stuttri lýsingu, skrifar ítarlegt issue (hegðun, útfærsla, samþykktarskilyrði, utan sviðs) og stofnar það í GitLab eða GitHub eftir samþykki.
argument-hint: "[stutt lýsing á verkinu]"
disable-model-invocation: false
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
   - GitLab: notaðu REST API-ið með Python (aðeins staðalsafnið), ekki `glab`. Lestu `<host>` og verkefnisslóðina (t.d. `hopur/verkefni`) úr `origin`. Skrifaðu textann í tímabundna skrá svo gæsalappir og línuskil skili sér rétt:

     ```bash
     python3 - "<host>" "<verkefnisslóð>" "<titill>" "<skrá með texta>" <<'EOF'
     import json, os, sys, urllib.error, urllib.parse, urllib.request

     host, project, title, body_file = sys.argv[1:]
     url = f"https://{host}/api/v4/projects/{urllib.parse.quote(project, safe='')}/issues"
     with open(body_file, encoding="utf-8") as f:
         data = urllib.parse.urlencode({"title": title, "description": f.read()}).encode()
     req = urllib.request.Request(url, data=data, headers={"PRIVATE-TOKEN": os.environ["GITLAB_TOKEN"]})
     try:
         issue = json.load(urllib.request.urlopen(req))
     except urllib.error.HTTPError as e:
         sys.exit(f"{e.code}: {e.read().decode()}")
     print(issue["iid"], issue["web_url"])
     EOF
     ```

     Skriftan prentar númer og slóð á issue-ið. Ekki prenta gildið á `GITLAB_TOKEN`.
   - GitHub: `gh issue create --title "<titill>" --body "<texti>"`

   Ef `GITLAB_TOKEN` er ekki sett (eða `gh` er ekki uppsett eða innskráð), eða kallið skilar villu: sýndu villuna og skilaðu textanum svo hægt sé að líma hann inn.
6. Skilaðu númeri og slóð á issue-ið.
