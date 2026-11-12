"""Task statistics response schema."""
from pydantic import BaseModel


class TaskStats(BaseModel):
    """Task statistics."""

    total: int
    pending: int
    completed: int
    high_priority: int
