"""Edge case tests for task management."""


def test_whitespace_only_title_invalid(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_whitespace_only_description_invalid(client):
    response = client.post("/tasks", json={"title": "Task", "description": "   "})
    assert response.status_code == 422


def test_whitespace_only_title_in_update(client):
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "   "})
    assert response.status_code == 422


def test_whitespace_only_description_in_update(client):
    create = client.post("/tasks", json={"title": "Task"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"description": "   "})
    assert response.status_code == 422


def test_invalid_status_filter(client):
    client.post("/tasks", json={"title": "Task"})

    response = client.get("/tasks?status=invalid")
    assert response.status_code == 400
    assert "Invalid status" in response.json()["detail"]


def test_invalid_priority_filter(client):
    client.post("/tasks", json={"title": "Task"})

    response = client.get("/tasks?priority=invalid")
    assert response.status_code == 400
    assert "Invalid priority" in response.json()["detail"]


def test_valid_filters_still_work(client):
    client.post("/tasks", json={"title": "Task 1", "status": "pending", "priority": "high"})

    response = client.get("/tasks?status=pending&priority=high")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_title_at_max_length_with_spaces(client):
    title = "a" * 98 + "  "
    response = client.post("/tasks", json={"title": title})
    assert response.status_code == 201
    assert response.json()["title"] == title


def test_description_empty_string_accepted(client):
    response = client.post("/tasks", json={"title": "Task", "description": ""})
    assert response.status_code == 201


def test_description_none_accepted(client):
    response = client.post("/tasks", json={"title": "Task", "description": None})
    assert response.status_code == 201
    assert response.json()["description"] is None


def test_update_only_allowed_fields(client):
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]
    original_created_at = create.json()["created_at"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "Updated"})
    assert response.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.json()["created_at"] == original_created_at
    assert get_resp.json()["title"] == "Updated"
