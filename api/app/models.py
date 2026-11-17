from datetime import datetime

from pydantic import BaseModel, Field


class Owner(BaseModel):
    id: int
    name: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    owner_id: int | None = None


class Task(BaseModel):
    id: int
    title: str
    is_complete: bool = False
    owner_id: int | None = None
    created_at: datetime
