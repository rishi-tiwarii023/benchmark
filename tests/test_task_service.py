from app.schemas.task import TaskCreate, TaskUpdate
from app.services import task as task_service


def test_service_crud(db_session):
    created = task_service.create_task(
        db_session, TaskCreate(title="Svc", description="d", status="pending")
    )
    assert created.id is not None
    assert created.title == "Svc"

    fetched = task_service.get_task(db_session, created.id)
    assert fetched is not None
    assert fetched.title == "Svc"

    tasks = task_service.list_tasks(db_session)
    assert len(tasks) == 1

    assert created.priority == "medium"

    updated = task_service.update_task(
        db_session,
        created.id,
        TaskUpdate(title="Svc updated", status="done", priority="high"),
    )
    assert updated is not None
    assert updated.title == "Svc updated"
    assert updated.status == "done"
    assert updated.priority == "high"

    refetched = task_service.get_task(db_session, created.id)
    assert refetched is not None
    assert refetched.title == "Svc updated"

    assert task_service.delete_task(db_session, created.id) is True
    assert task_service.get_task(db_session, created.id) is None
    assert task_service.delete_task(db_session, created.id) is False
