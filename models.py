from sqlmodel import SQLModel, Field
from datetime import date

class TaskBase(SQLModel):
    title: str = Field(min_length=2, max_length=50,index=True)
    priority: int = Field(ge=1, index=True)
    description: str | None = Field(default=None, max_length=300)
    due_date: date | None = Field(default=None)

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)