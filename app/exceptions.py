"""Custom exceptions for the application."""
from fastapi import HTTPException, status


class TaskNotFound(HTTPException):
    """Raised when a task is not found."""

    def __init__(self, task_id: int = None):
        detail = "Task not found"
        if task_id:
            detail = f"Task with id {task_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
