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
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "New"
    assert get_resp.json()["status"] == "done"


def test_delete_task(client):
    create = client.post("/tasks", json={"title": "Remove me"})
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_get_missing_task_404(client):
    assert client.get("/tasks/9999").status_code == 404


def test_create_task_default_priority(client):
    response = client.post("/tasks", json={"title": "Default priority"})
    assert response.status_code == 201
    assert response.json()["priority"] == "medium"


def test_create_task_with_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Urgent", "priority": "high"},
    )
    assert response.status_code == 201
    assert response.json()["priority"] == "high"

    get_resp = client.get(f"/tasks/{response.json()['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["priority"] == "high"


def test_update_task_priority(client):
    create = client.post("/tasks", json={"title": "Reprioritize", "priority": "low"})
    task_id = create.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"priority": "high"})
    assert response.status_code == 200
    assert response.json()["priority"] == "high"


def test_create_task_invalid_priority_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Bad", "priority": "critical"},
    )
    assert response.status_code == 422


def test_list_tasks_filter_by_status(client):
    client.post("/tasks", json={"title": "Pending one", "status": "pending"})
    client.post("/tasks", json={"title": "Done one", "status": "done"})
    response = client.get("/tasks", params={"status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pending one"
    assert data[0]["status"] == "pending"


def test_list_tasks_filter_by_priority(client):
    client.post("/tasks", json={"title": "High", "priority": "high"})
    client.post("/tasks", json={"title": "Low", "priority": "low"})
    response = client.get("/tasks", params={"priority": "high"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "High"
    assert data[0]["priority"] == "high"


def test_list_tasks_filter_by_status_and_priority(client):
    client.post(
        "/tasks",
        json={"title": "Match", "status": "pending", "priority": "high"},
    )
    client.post(
        "/tasks",
        json={"title": "Wrong status", "status": "done", "priority": "high"},
    )
    client.post(
        "/tasks",
        json={"title": "Wrong priority", "status": "pending", "priority": "low"},
    )
    response = client.get("/tasks", params={"status": "pending", "priority": "high"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Match"


def test_list_tasks_pagination_limit_offset(client):
    for i in range(15):
        client.post("/tasks", json={"title": f"Task {i}"})
    response = client.get("/tasks", params={"limit": 10, "offset": 0})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert [t["title"] for t in data] == [f"Task {i}" for i in range(10)]

    page2 = client.get("/tasks", params={"limit": 10, "offset": 10})
    assert page2.status_code == 200
    assert len(page2.json()) == 5
    assert page2.json()[0]["title"] == "Task 10"


def test_list_tasks_default_pagination_limit(client):
    for i in range(25):
        client.post("/tasks", json={"title": f"T{i}"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_list_tasks_invalid_pagination_422(client):
    for params in ({"limit": 0}, {"limit": 101}, {"limit": -1}, {"offset": -1}):
        assert client.get("/tasks", params=params).status_code == 422


def test_list_tasks_pagination_with_status_filter(client):
    for i in range(5):
        client.post(
            "/tasks",
            json={"title": f"P{i}", "status": "pending"},
        )
    client.post("/tasks", json={"title": "Done", "status": "done"})
    response = client.get(
        "/tasks",
        params={"status": "pending", "limit": 2, "offset": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["status"] == "pending" for t in data)
    assert data[0]["title"] == "P1"
