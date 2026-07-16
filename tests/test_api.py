from fastapi.testclient import TestClient

from database import create_db_and_tables

from main import app

create_db_and_tables()

client = TestClient(app)


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "priority": 1,
            "description": "Study",
            "due_date": None
        }
    )
    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == 1
    assert data["description"] == "Study"
    assert data["due_date"] == None
    assert data["completed"] == False

def test_unique_title():
    response1 = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "priority": 1
        }
    )

    assert response1.status_code == 200

    response2 = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "priority": 1
        }
    ) 
    assert response2.status_code == 400

def test_update_prio():
    response1 = client.post(
        "/tasks/",
        json={
            "title": "Title1",
            "priority": 1
        }
    )

    data = response1.json()
    assert data["priority"] == 1

    response2 = client.post(
        "/tasks/",
        json={
            "title": "Title2",
            "priority": 2
        }
    )

    data = response2.json()
    assert data["priority"] == 2

    response3 = client.post(
        "/tasks/",
        json={
            "title": "Title3",
            "priority": 1
        }
    )

    data = response3.json()
    assert data["priority"] == 1

    update1 = client.get("/tasks/search?title=Title1")
    data = update1.json()
    assert data[0]["priority"] == 2

    update2 = client.get("/tasks/search?title=Title2")
    data = update2.json()
    assert data[0]["priority"] == 3





    