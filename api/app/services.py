from datetime import UTC, datetime

from .models import Owner, Task, TaskCreate


class OwnerNotFound(Exception):
    pass


class TaskService:
    """In-memory store. Data is lost on restart, by design."""

    def __init__(self) -> None:
        self._owners: dict[int, Owner] = {}
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add_owner(self, name: str) -> Owner:
        owner = Owner(id=len(self._owners) + 1, name=name)
        self._owners[owner.id] = owner
        return owner

    def list_owners(self) -> list[Owner]:
        return list(self._owners.values())

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def add_task(self, data: TaskCreate) -> Task:
        if data.owner_id is not None and data.owner_id not in self._owners:
            raise OwnerNotFound(data.owner_id)
        task = Task(
            id=self._next_id,
            title=data.title,
            owner_id=data.owner_id,
            created_at=datetime.now(UTC),
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task


def seeded_service() -> TaskService:
    """Synthetic demo data only. No real names."""
    service = TaskService()
    anna = service.add_owner("Anna Dæmisdóttir")
    bjorn = service.add_owner("Björn Prufuson")
    service.add_task(TaskCreate(title="Yfirfara skýrslu", owner_id=anna.id))
    service.add_task(TaskCreate(title="Uppfæra leiðbeiningar", owner_id=bjorn.id))
    service.add_task(TaskCreate(title="Svara fyrirspurn"))
    return service
