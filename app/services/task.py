from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.id).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(title=data.title, description=data.description, status=data.status)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task | None:
    task = get_task(db, task_id)
    if task is None:
        return None
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    task = get_task(db, task_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True
