"""Task repository for data access operations."""
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    """Encapsulates all task database operations."""

    def __init__(self, db: Session):
        self.db = db

    def list_all(
        self,
        status: str | None = None,
        priority: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Task]:
        """List tasks with optional filtering and pagination."""
        query = self.db.query(Task)
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        return query.order_by(Task.id).limit(limit).offset(offset).all()

    def get_by_id(self, task_id: int) -> Task | None:
        """Get a single task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, task: Task) -> Task:
        """Create a new task."""
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task, updates: dict) -> Task:
        """Update an existing task.

        Only allows updating: title, description, status, priority.
        Prevents accidental updates to id, created_at, etc.
        """
        allowed_fields = {"title", "description", "status", "priority"}
        for key, value in updates.items():
            if key in allowed_fields:
                setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        """Delete a task."""
        self.db.delete(task)
        self.db.commit()

    def get_stats(self) -> dict:
        """Get task statistics."""
        total = self.db.query(func.count(Task.id)).scalar() or 0
        pending = self.db.query(func.count(Task.id)).filter(Task.status == "pending").scalar() or 0
        completed = self.db.query(func.count(Task.id)).filter(Task.status == "done").scalar() or 0
        high_priority = self.db.query(func.count(Task.id)).filter(Task.priority == "high").scalar() or 0

        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "high_priority": high_priority,
        }
