"""Task business logic services."""
from sqlalchemy.orm import Session

from app.models.task import Task
from app.repository.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


def get_repository(db: Session) -> TaskRepository:
    """Get a task repository instance."""
    return TaskRepository(db)


def list_tasks(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Task]:
    """List tasks with optional filtering and pagination."""
    repo = get_repository(db)
    return repo.list_all(status=status, priority=priority, limit=limit, offset=offset)


def get_task(db: Session, task_id: int) -> Task | None:
    """Get a single task by ID."""
    repo = get_repository(db)
    return repo.get_by_id(task_id)


def create_task(db: Session, data: TaskCreate) -> Task:
    """Create a new task."""
    repo = get_repository(db)
    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
    )
    return repo.create(task)


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task | None:
    """Update an existing task."""
    repo = get_repository(db)
    task = repo.get_by_id(task_id)
    if task is None:
        return None
    updates = data.model_dump(exclude_unset=True)
    return repo.update(task, updates)


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task."""
    repo = get_repository(db)
    task = repo.get_by_id(task_id)
    if task is None:
        return False
    repo.delete(task)
    return True


def get_stats(db: Session) -> dict:
    """Get task statistics."""
    repo = get_repository(db)
    return repo.get_stats()
