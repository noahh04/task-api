from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from database import create_db_and_tables, SessionDep
from models import Task
from schemas import TaskCreate, TaskPublic, TaskUpdate

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def update_prio_increase(tasks_to_be_updated):
    for task in tasks_to_be_updated:
        task.priority += 1

def update_prio_decrease(tasks_to_be_updated):
    for task in tasks_to_be_updated:
        task.priority -= 1


@app.post("/tasks/", response_model=TaskPublic)
def create_task(task: TaskCreate, session: SessionDep):

    #error when task with same title already exists
    existing_task = session.exec(select(Task).where(Task.title == task.title)).first()
    if existing_task:
        raise HTTPException(status_code=400, detail = f"Task with title {existing_task.title} already exists")
    
    #error when user wants to set tasks's priority higher than existing tasks
    all_tasks = session.exec(select(Task)).all()
    if task.priority > len(all_tasks) + 1:
        raise HTTPException(status_code=400, detail = f"The task's priority can't be higher than {len(all_tasks) + 1}")

    task_db = Task.model_validate(task)

    #when user wants a new task to have higher prio than existing task/tasks, all tasks behind get prio+1
    tasks_to_be_updated = session.exec(select(Task).where(Task.priority >= task.priority, Task.id != task_db.id)).all()
    if tasks_to_be_updated:
        update_prio_increase(tasks_to_be_updated)

    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@app.get("/tasks/", response_model=list[TaskPublic])
def show_all_tasks (
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@app.get("/tasks/search", response_model=list[TaskPublic])
def search_for_task (
    session: SessionDep,
    title: str | None = None,
    max_prio: int | None = None
):
    query = select(Task)

    if title:
        query = query.where(Task.title.contains(title))

    if max_prio:
        query = query.where(Task.priority <= max_prio)
    
    tasks = session.exec(query).all()

    return tasks



@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task_by_id (task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, task: TaskUpdate, session: SessionDep):
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    old_prio = task_db.priority
    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)

    #error when user wants to set tasks's priority higher than existing tasks
    if task_db.priority != None:
        all_tasks = session.exec(select(Task)).all()
        if task_db.priority > len(all_tasks) + 1:
            raise HTTPException(status_code=400, detail = f"The task's priority can't be higher than {len(all_tasks) + 1}")

    #when user wants an existing task to have higher prio, all tasks behind get prio+1
    if task_db.priority < old_prio:
        tasks_to_be_updated = session.exec(select(Task).where(Task.priority >= task_db.priority, Task.priority < old_prio, Task.id != task_db.id)).all()
        if tasks_to_be_updated:
            update_prio_increase(tasks_to_be_updated)
    #when user wants an existing task to have lower prio, all tasks behind get prio-1
    if task_db.priority > old_prio:
        tasks_to_be_updated = session.exec(select(Task).where(Task.priority <= task_db.priority, Task.priority > old_prio, Task.id != task_db.id)).all()
        if tasks_to_be_updated:
            update_prio_decrease(tasks_to_be_updated)

    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_to_be_updated = session.exec(select(Task).where(Task.priority > task.priority)).all()
    if tasks_to_be_updated:
        update_prio_decrease(tasks_to_be_updated)

    session.delete(task)
    session.commit()
    return {"deleted successfully": True}
