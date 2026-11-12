import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Valid", "description": "ok", "status": "pending", "priority": "low"},
        {"title": "x" * 100, "description": "y" * 500},
        {"title": "Minimal"},
    ],
)
def test_create_valid_inputs(client, payload):
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    if "description" in payload:
        assert body["description"] == payload["description"]


@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "   "},
        {"title": "x" * 101},
        {"title": "Ok", "description": "d" * 501},
        {"title": "Ok", "status": "archived"},
        {"title": "Ok", "priority": "urgent"},
    ],
)
def test_create_invalid_inputs_422(client, payload):
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_create_missing_title_422(client):
    assert client.post("/tasks", json={"description": "only desc"}).status_code == 422


def test_update_valid_title_and_status(client):
    task_id = client.post("/tasks", json={"title": "Before"}).json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "After", "status": "done", "priority": "high"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "After"
    assert body["status"] == "done"
    assert body["priority"] == "high"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "   "},
        {"title": "x" * 101},
        {"description": "d" * 501},
        {"status": "invalid"},
        {"priority": "critical"},
    ],
)
def test_update_invalid_inputs_422(client, payload):
    task_id = client.post("/tasks", json={"title": "Seed"}).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 422


def test_list_tasks_invalid_status_filter_422(client):
    assert client.get("/tasks", params={"status": "bogus"}).status_code == 422


def test_list_tasks_invalid_priority_filter_422(client):
    assert client.get("/tasks", params={"priority": "bogus"}).status_code == 422
