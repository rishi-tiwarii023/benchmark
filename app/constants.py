"""Application-wide constants for task management."""

# Valid task status values
VALID_STATUSES = {"pending", "in_progress", "done"}
STATUS_PATTERN = "^(pending|in_progress|done)$"

# Valid task priority values
VALID_PRIORITIES = {"low", "medium", "high"}
PRIORITY_PATTERN = "^(low|medium|high)$"

# Default values
DEFAULT_STATUS = "pending"
DEFAULT_PRIORITY = "medium"

# Pagination defaults
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
DEFAULT_OFFSET = 0
