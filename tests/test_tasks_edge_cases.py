def test_patch_missing_task_404(client):
    assert client.patch("/tasks/9999", json={"title": "Nope"}).status_code == 404


def test_delete_missing_task_404(client):
    assert client.delete("/tasks/9999").status_code == 404


def test_patch_empty_body_returns_unchanged_task(client):
    create = client.post("/tasks", json={"title": "Stable", "status": "pending"})
    task_id = create.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Stable"
    assert body["status"] == "pending"


def test_list_tasks_offset_beyond_total_returns_empty(client):
    client.post("/tasks", json={"title": "Only"})
    response = client.get("/tasks", params={"limit": 10, "offset": 100})
    assert response.status_code == 200
    assert response.json() == []


def test_stats_reflect_task_deletion(client):
    task_id = client.post("/tasks", json={"title": "Gone", "status": "pending"}).json()["id"]
    assert client.get("/tasks/stats").json()["total"] == 1
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get("/tasks/stats").json() == {
        "total": 0,
        "pending": 0,
        "completed": 0,
        "high_priority": 0,
    }


def test_tasks_stats_route_not_shadowed_by_task_id(client):
    response = client.get("/tasks/stats")
    assert response.status_code == 200
    assert set(response.json().keys()) == {
        "total",
        "pending",
        "completed",
        "high_priority",
    }
