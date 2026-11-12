def test_create_and_get_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Buy milk", "description": "2%", "status": "pending"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == "2%"
    assert body["status"] == "pending"
    assert "id" in body
    assert "created_at" in body

    task_id = body["id"]
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == task_id


def test_list_tasks(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_task(client):
    create = client.post("/tasks", json={"title": "Old", "status": "pending"})
    task_id = create.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "New", "status": "done"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New"
    assert response.json()["status"] == "done"


def test_delete_task(client):
    create = client.post("/tasks", json={"title": "Remove me"})
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_get_missing_task_404(client):
    assert client.get("/tasks/9999").status_code == 404
