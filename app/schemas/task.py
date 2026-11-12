from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.constants import (
    DEFAULT_PRIORITY,
    DEFAULT_STATUS,
    PRIORITY_PATTERN,
    STATUS_PATTERN,
)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    status: str = Field(DEFAULT_STATUS, pattern=STATUS_PATTERN)
    priority: str = Field(DEFAULT_PRIORITY, pattern=PRIORITY_PATTERN)

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v):
        """Ensure title is not only whitespace."""
        if v and not v.strip():
            raise ValueError("title cannot be only whitespace")
        return v

    @field_validator("description")
    @classmethod
    def description_not_whitespace(cls, v):
        """Ensure description is not only whitespace (but empty string is OK)."""
        if v is not None and v and not v.strip():
            raise ValueError("description cannot be only whitespace")
        return v


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    status: str | None = Field(None, pattern=STATUS_PATTERN)
    priority: str | None = Field(None, pattern=PRIORITY_PATTERN)

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v):
        """Ensure title is not only whitespace."""
        if v is not None and not v.strip():
            raise ValueError("title cannot be only whitespace")
        return v

    @field_validator("description")
    @classmethod
    def description_not_whitespace(cls, v):
        """Ensure description is not only whitespace (but empty string is OK)."""
        if v is not None and v and not v.strip():
            raise ValueError("description cannot be only whitespace")
        return v


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime
