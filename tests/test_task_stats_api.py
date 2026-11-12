def test_task_stats_empty_database(client):
    response = client.get("/tasks/stats")
    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "pending": 0,
        "completed": 0,
        "high_priority": 0,
    }


def test_task_stats_counts_from_database(client):
    client.post("/tasks", json={"title": "P1", "status": "pending", "priority": "high"})
    client.post("/tasks", json={"title": "P2", "status": "pending", "priority": "low"})
    client.post(
        "/tasks",
        json={"title": "D1", "status": "done", "priority": "high"},
    )
    client.post(
        "/tasks",
        json={"title": "D2", "status": "done", "priority": "medium"},
    )
    client.post("/tasks", json={"title": "P3", "status": "pending", "priority": "high"})

    response = client.get("/tasks/stats")
    assert response.status_code == 200
    assert response.json() == {
        "total": 5,
        "pending": 3,
        "completed": 2,
        "high_priority": 3,
    }
