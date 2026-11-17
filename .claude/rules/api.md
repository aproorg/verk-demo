---
paths:
  - "api/**/*.py"
---

# API-reglur

- Endapunktar í `main.py` eru þunnir: þeir kalla á `TaskService` og þýða niðurstöðuna í HTTP-svar
- Þjónustan kastar eigin undantekningum (t.d. `OwnerNotFound`). Aðeins `main.py` þekkir `HTTPException`
- Notaðu `Service`-týpuna (`Annotated[TaskService, Depends(get_service)]`) fyrir dependency injection
- Próf nota `client`- og `service`-fixture í `tests/test_tasks.py`, aldrei gögnin úr `seeded_service()`
- Skilatýpur eru Pydantic-líkön, ekki `dict`
