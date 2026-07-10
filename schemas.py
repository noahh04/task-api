from sqlmodel import SQLModel, Field
from models import TaskBase
from datetime import date



class TaskPublic(TaskBase):
    id: int
    completed: bool


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    priority: int | None = Field(default=None, ge=1)
    description: str | None = None
    due_date: date | None = None
    completed: bool | None = None
