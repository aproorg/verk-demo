from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from .models import Owner, Task, TaskCreate
from .services import OwnerNotFound, TaskService, seeded_service

app = FastAPI(title="Verk API")

_service = seeded_service()


def get_service() -> TaskService:
    return _service


Service = Annotated[TaskService, Depends(get_service)]


@app.get("/owners")
def list_owners(service: Service) -> list[Owner]:
    return service.list_owners()


@app.get("/tasks")
def list_tasks(service: Service) -> list[Task]:
    return service.list_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int, service: Service) -> Task:
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=201)
def add_task(data: TaskCreate, service: Service) -> Task:
    try:
        return service.add_task(data)
    except OwnerNotFound:
        raise HTTPException(status_code=422, detail="Owner not found") from None
