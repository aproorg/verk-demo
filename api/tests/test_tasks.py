import pytest
from fastapi.testclient import TestClient

from app.main import app, get_service
from app.models import TaskCreate
from app.services import OwnerNotFound, TaskService


@pytest.fixture
def service() -> TaskService:
    service = TaskService()
    service.add_owner("Prufa Prufudóttir")
    return service


@pytest.fixture
def client(service: TaskService):
    app.dependency_overrides[get_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


# --- service ---


def test_new_task_is_not_complete(service: TaskService):
    task = service.add_task(TaskCreate(title="Skrifa próf", owner_id=1))
    assert task.id == 1
    assert task.is_complete is False


def test_unknown_owner_is_rejected(service: TaskService):
    with pytest.raises(OwnerNotFound):
        service.add_task(TaskCreate(title="Skrifa próf", owner_id=99))


# --- endpoints ---


def test_create_and_list_tasks(client: TestClient):
    created = client.post("/tasks", json={"title": "Skrifa próf", "owner_id": 1})
    assert created.status_code == 201
    assert [t["title"] for t in client.get("/tasks").json()] == ["Skrifa próf"]


def test_missing_task_returns_404(client: TestClient):
    assert client.get("/tasks/42").status_code == 404


def test_empty_title_returns_422(client: TestClient):
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_unknown_owner_returns_422(client: TestClient):
    assert client.post("/tasks", json={"title": "x", "owner_id": 99}).status_code == 422
