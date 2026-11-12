"""Task API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query, status as http_status
from sqlalchemy.orm import Session

from app.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    VALID_PRIORITIES,
    VALID_STATUSES,
)
from app.database.session import get_db
from app.exceptions import TaskNotFound
from app.schemas.stats import TaskStats
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import task as task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/stats", response_model=TaskStats)
def get_task_stats(db: Session = Depends(get_db)):
    """Get task statistics."""
    stats = task_service.get_stats(db)
    return stats


@router.get("", response_model=list[TaskRead])
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    offset: int = Query(DEFAULT_OFFSET, ge=0),
    db: Session = Depends(get_db),
):
    """List tasks with optional filtering and pagination."""
    if status is not None and status not in VALID_STATUSES:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_STATUSES))}",
        )
    if priority is not None and priority not in VALID_PRIORITIES:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid priority. Must be one of: {', '.join(sorted(VALID_PRIORITIES))}",
        )
    return task_service.list_tasks(db, status=status, priority=priority, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID."""
    task = task_service.get_task(db, task_id)
    if task is None:
        raise TaskNotFound(task_id)
    return task


@router.post("", response_model=TaskRead, status_code=http_status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    return task_service.create_task(db, data)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task."""
    task = task_service.update_task(db, task_id, data)
    if task is None:
        raise TaskNotFound(task_id)
    return task


@router.delete("/{task_id}", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    if not task_service.delete_task(db, task_id):
        raise TaskNotFound(task_id)
