from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import task as task_repository
from app.schemas.task import TaskCreate, TaskStats, TaskUpdate


def list_tasks(
    db: Session,
    *,
    status: str | None = None,
    priority: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Task]:
    return task_repository.find_many(
        db,
        status=status,
        priority=priority,
        limit=limit,
        offset=offset,
    )


def get_task(db: Session, task_id: int) -> Task | None:
    return task_repository.find_by_id(db, task_id)


def get_task_stats(db: Session) -> TaskStats:
    return TaskStats(**task_repository.count_stats(db))


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
    )
    return task_repository.add(db, task)


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task | None:
    task = task_repository.find_by_id(db, task_id)
    if task is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    return task_repository.persist(db, task)


def delete_task(db: Session, task_id: int) -> bool:
    task = task_repository.find_by_id(db, task_id)
    if task is None:
        return False
    task_repository.remove(db, task)
    return True
