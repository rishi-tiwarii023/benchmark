

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
    assert stats["high_priority"] == 5


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
