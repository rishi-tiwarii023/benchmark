# Task Manager (FastAPI)

Minimal task manager API with SQLite and SQLAlchemy.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Tests

```bash
pytest
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks` | List tasks |
| GET | `/tasks/{id}` | Get task |
| POST | `/tasks` | Create task |
| PATCH | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

Task fields: `id`, `title`, `description`, `status`, `created_at` (default status: `pending`).
