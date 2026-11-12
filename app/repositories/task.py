from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.task import Task


def find_many(
    db: Session,
    *,
    status: str | None = None,
    priority: str | None = None,
    limit: int,
    offset: int,
) -> list[Task]:
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status)
    if priority is not None:
        query = query.filter(Task.priority == priority)
    return query.order_by(Task.id).offset(offset).limit(limit).all()


def find_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def count_stats(db: Session) -> dict[str, int]:
    total = db.query(func.count(Task.id)).scalar()
    pending = (
        db.query(func.count(Task.id)).filter(Task.status == "pending").scalar()
    )
    completed = db.query(func.count(Task.id)).filter(Task.status == "done").scalar()
    high_priority = (
        db.query(func.count(Task.id)).filter(Task.priority == "high").scalar()
    )
    return {
        "total": int(total or 0),
        "pending": int(pending or 0),
        "completed": int(completed or 0),
        "high_priority": int(high_priority or 0),
    }


def add(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def persist(db: Session, task: Task) -> Task:
    db.commit()
    db.refresh(task)
    return task


def remove(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
