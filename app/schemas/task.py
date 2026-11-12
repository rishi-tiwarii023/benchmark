from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

TaskPriority = Literal["low", "medium", "high"]
TaskStatus = Literal["pending", "done"]


def _reject_blank_title(value: str) -> str:
    if not value.strip():
        raise ValueError("title cannot be empty")
    return value


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    status: TaskStatus = "pending"
    priority: TaskPriority = "medium"

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        return _reject_blank_title(value)


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _reject_blank_title(value)


class TaskStats(BaseModel):
    total: int
    pending: int
    completed: int
    high_priority: int


class TaskListParams(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
