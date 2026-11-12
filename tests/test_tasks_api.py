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


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_default_priority(client):
    response = client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["priority"] == "medium"


def test_create_task_with_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Urgent", "priority": "high"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["priority"] == "high"

    task_id = body["id"]
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["priority"] == "high"


def test_update_task_priority(client):
    create = client.post("/tasks", json={"title": "Task", "priority": "low"})
    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": "high"},
    )
    assert response.status_code == 200
    assert response.json()["priority"] == "high"


def test_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Test", "priority": "invalid"},
    )
    assert response.status_code == 422


def test_filter_by_status(client):
    client.post("/tasks", json={"title": "Task 1", "status": "pending"})
    client.post("/tasks", json={"title": "Task 2", "status": "done"})
    client.post("/tasks", json={"title": "Task 3", "status": "pending"})

    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert all(task["status"] == "pending" for task in tasks)


def test_filter_by_priority(client):
    client.post("/tasks", json={"title": "Task 1", "priority": "high"})
    client.post("/tasks", json={"title": "Task 2", "priority": "low"})
    client.post("/tasks", json={"title": "Task 3", "priority": "high"})

    response = client.get("/tasks?priority=high")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert all(task["priority"] == "high" for task in tasks)


def test_filter_by_status_and_priority(client):
    client.post("/tasks", json={"title": "Task 1", "status": "pending", "priority": "high"})
    client.post("/tasks", json={"title": "Task 2", "status": "pending", "priority": "low"})
    client.post("/tasks", json={"title": "Task 3", "status": "done", "priority": "high"})

    response = client.get("/tasks?status=pending&priority=high")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "pending"
    assert tasks[0]["priority"] == "high"


def test_filter_no_results(client):
    client.post("/tasks", json={"title": "Task 1", "status": "pending"})

    response = client.get("/tasks?status=done")
    assert response.status_code == 200
    assert response.json() == []


# Input Validation Tests

def test_valid_task_creation(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Valid Task",
            "description": "Valid description",
            "status": "in_progress",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Valid Task"
    assert body["description"] == "Valid description"
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"


def test_empty_title_invalid(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_title_too_long_invalid(client):
    long_title = "a" * 101
    response = client.post("/tasks", json={"title": long_title})
    assert response.status_code == 422


def test_title_max_length_valid(client):
    max_title = "a" * 100
    response = client.post("/tasks", json={"title": max_title})
    assert response.status_code == 201
    assert response.json()["title"] == max_title


def test_description_too_long_invalid(client):
    long_description = "b" * 501
    response = client.post(
        "/tasks",
        json={"title": "Test", "description": long_description},
    )
    assert response.status_code == 422


def test_description_max_length_valid(client):
    max_description = "b" * 500
    response = client.post(
        "/tasks",
        json={"title": "Test", "description": max_description},
    )
    assert response.status_code == 201
    assert response.json()["description"] == max_description


def test_invalid_status_value(client):
    response = client.post(
        "/tasks",
        json={"title": "Test", "status": "invalid_status"},
    )
    assert response.status_code == 422


def test_valid_status_values(client):
    for status in ["pending", "in_progress", "done"]:
        response = client.post(
            "/tasks",
            json={"title": f"Task {status}", "status": status},
        )
        assert response.status_code == 201
        assert response.json()["status"] == status


def test_invalid_priority_value(client):
    response = client.post(
        "/tasks",
        json={"title": "Test", "priority": "invalid_priority"},
    )
    assert response.status_code == 422


def test_valid_priority_values(client):
    for priority in ["low", "medium", "high"]:
        response = client.post(
            "/tasks",
            json={"title": f"Task {priority}", "priority": priority},
        )
        assert response.status_code == 201
        assert response.json()["priority"] == priority


def test_update_with_invalid_title(client):
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""},
    )
    assert response.status_code == 422


def test_update_with_invalid_status(client):
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "invalid"},
    )
    assert response.status_code == 422


def test_update_with_valid_values(client):
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated",
            "description": "Updated description",
            "status": "done",
            "priority": "low",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated"
    assert body["description"] == "Updated description"
    assert body["status"] == "done"
    assert body["priority"] == "low"


# Pagination Tests

def test_pagination_default_limit(client):
    for i in range(25):
        client.post("/tasks", json={"title": f"Task {i}"})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 20


def test_pagination_custom_limit(client):
    for i in range(25):
        client.post("/tasks", json={"title": f"Task {i}"})

    response = client.get("/tasks?limit=10")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 10


def test_pagination_with_offset(client):
    for i in range(25):
        client.post("/tasks", json={"title": f"Task {i}"})

    # First page
    response1 = client.get("/tasks?limit=10&offset=0")
    assert response1.status_code == 200
    tasks1 = response1.json()
    assert len(tasks1) == 10

    # Second page
    response2 = client.get("/tasks?limit=10&offset=10")
    assert response2.status_code == 200
    tasks2 = response2.json()
    assert len(tasks2) == 10

    # Verify pages are different
    ids1 = {t["id"] for t in tasks1}
    ids2 = {t["id"] for t in tasks2}
    assert ids1.isdisjoint(ids2)


def test_pagination_limit_zero_invalid(client):
    response = client.get("/tasks?limit=0")
    assert response.status_code == 422


def test_pagination_limit_exceeds_max(client):
    response = client.get("/tasks?limit=101")
    assert response.status_code == 422


def test_pagination_negative_offset_invalid(client):
    response = client.get("/tasks?offset=-1")
    assert response.status_code == 422


def test_pagination_with_filtering(client):
    for i in range(15):
        status = "pending" if i % 2 == 0 else "done"
        client.post("/tasks", json={"title": f"Task {i}", "status": status})

    # Filter by status with pagination
    response = client.get("/tasks?status=pending&limit=5&offset=0")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) <= 5
    assert all(t["status"] == "pending" for t in tasks)


def test_pagination_with_priority_filter(client):
    for i in range(15):
        priority = "high" if i % 3 == 0 else "low"
        client.post("/tasks", json={"title": f"Task {i}", "priority": priority})

    # Filter by priority with pagination
    response = client.get("/tasks?priority=high&limit=5&offset=0")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["priority"] == "high" for t in tasks)


def test_pagination_all_filters_together(client):
    for i in range(20):
        status = "pending" if i % 2 == 0 else "done"
        priority = "high" if i % 3 == 0 else "medium"
        client.post("/tasks", json={
            "title": f"Task {i}",
            "status": status,
            "priority": priority
        })

    response = client.get("/tasks?status=pending&priority=high&limit=5&offset=0")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "pending" and t["priority"] == "high" for t in tasks)


def test_pagination_beyond_available_data(client):
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}"})

    response = client.get("/tasks?limit=10&offset=10")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 0


def test_pagination_max_limit_accepted(client):
    for i in range(101):
        client.post("/tasks", json={"title": f"Task {i}"})

    response = client.get("/tasks?limit=100")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 100


# Statistics Tests

def test_stats_empty_database(client):
    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 0
    assert stats["pending"] == 0
    assert stats["completed"] == 0
    assert stats["high_priority"] == 0


def test_stats_with_tasks(client):
    client.post("/tasks", json={"title": "Task 1", "status": "pending", "priority": "high"})
    client.post("/tasks", json={"title": "Task 2", "status": "pending", "priority": "medium"})
    client.post("/tasks", json={"title": "Task 3", "status": "pending", "priority": "low"})
    client.post("/tasks", json={"title": "Task 4", "status": "done", "priority": "high"})
    client.post("/tasks", json={"title": "Task 5", "status": "done", "priority": "high"})
    client.post("/tasks", json={"title": "Task 6", "status": "in_progress", "priority": "medium"})

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 6
    assert stats["pending"] == 3
    assert stats["completed"] == 2
    assert stats["high_priority"] == 3


def test_stats_all_completed(client):
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}", "status": "done"})

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 5
    assert stats["pending"] == 0
    assert stats["completed"] == 5
    assert stats["high_priority"] == 0


def test_stats_all_high_priority(client):
    for i in range(4):
        client.post("/tasks", json={"title": f"Task {i}", "priority": "high"})

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 4
    assert stats["pending"] == 4
    assert stats["completed"] == 0
    assert stats["high_priority"] == 4


def test_stats_mixed_scenarios(client):
    tasks_data = [
        {"title": "Task 1", "status": "pending", "priority": "high"},
        {"title": "Task 2", "status": "pending", "priority": "high"},
        {"title": "Task 3", "status": "pending", "priority": "medium"},
        {"title": "Task 4", "status": "pending", "priority": "low"},
        {"title": "Task 5", "status": "in_progress", "priority": "high"},
        {"title": "Task 6", "status": "in_progress", "priority": "medium"},
        {"title": "Task 7", "status": "done", "priority": "high"},
        {"title": "Task 8", "status": "done", "priority": "medium"},
        {"title": "Task 9", "status": "done", "priority": "low"},
        {"title": "Task 10", "status": "done", "priority": "low"},
    ]

    for task_data in tasks_data:
        client.post("/tasks", json=task_data)

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 10
    assert stats["pending"] == 4
    assert stats["completed"] == 4
    assert stats["high_priority"] == 4


def test_stats_after_updates(client):
    create_resp = client.post("/tasks", json={"title": "Task", "status": "pending", "priority": "low"})
    task_id = create_resp.json()["id"]

    stats_resp = client.get("/tasks/stats")
    assert stats_resp.json()["pending"] == 1
    assert stats_resp.json()["completed"] == 0
    assert stats_resp.json()["high_priority"] == 0

    client.patch(f"/tasks/{task_id}", json={"status": "done", "priority": "high"})

    stats_resp = client.get("/tasks/stats")
    stats = stats_resp.json()
    assert stats["pending"] == 0
    assert stats["completed"] == 1
    assert stats["high_priority"] == 1


def test_stats_after_deletion(client):
    for i in range(3):
        client.post("/tasks", json={"title": f"Task {i}", "priority": "high"})

    stats_resp = client.get("/tasks/stats")
    assert stats_resp.json()["total"] == 3
    assert stats_resp.json()["high_priority"] == 3

    tasks_resp = client.get("/tasks?limit=1")
    task_id = tasks_resp.json()[0]["id"]
    client.delete(f"/tasks/{task_id}")

    stats_resp = client.get("/tasks/stats")
    stats = stats_resp.json()
    assert stats["total"] == 2
    assert stats["high_priority"] == 2


def test_stats_response_format(client):
    client.post("/tasks", json={"title": "Task 1"})

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    stats = response.json()

    assert isinstance(stats["total"], int)
    assert isinstance(stats["pending"], int)
    assert isinstance(stats["completed"], int)
    assert isinstance(stats["high_priority"], int)

    assert set(stats.keys()) == {"total", "pending", "completed", "high_priority"}
