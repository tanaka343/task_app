from fastapi.testclient import TestClient

def test_find_all(client_fixture :TestClient):
    response = client_fixture.get("/tasks")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2

def test_find_by_due_正常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/?due_date=2025-10-30&end=7")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1

def test_find_by_due_異常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/?due_date=2024-11-30&end=7")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_find_by_due_fromtoday_正常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/today/?end=7")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1

def test_find_by_due_fromtoday_異常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/today/?end=-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_find_by_id_正常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    
def test_find_by_id_異常系(client_fixture :TestClient):
    response = client_fixture.get("/tasks/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create(client_fixture :TestClient):
    response = client_fixture.post("/tasks",json={"title":"kaimono3","content":"banana","due_date":"2025-11-04","completed":False})
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["title"] == "kaimono3"
    assert item["content"] == "banana"
    assert item["due_date"] == "2025-11-04"
    assert item["completed"] == False
    response = client_fixture.get("/tasks")
    assert len(response.json()) == 3

def test_update_正常系(client_fixture :TestClient):
    response = client_fixture.put("/tasks/1",json={"title":"kaimono4","content":"apple","due_date":"2025-11-04","completed":True})
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["title"] == "kaimono4"
    assert item["content"] == "apple"
    assert item["due_date"] == "2025-11-04"
    assert item["completed"] == True

def test_update_異常系(client_fixture :TestClient):
    response = client_fixture.put("/tasks/10",json={"title":"kaimono4","content":"apple","due_date":"2025-11-04","completed":True})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_delete_正常系(client_fixture :TestClient):
    response = client_fixture.delete("/tasks/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    response = client_fixture.get("/tasks")
    assert len(response.json()) == 1

def test_delete_異常系(client_fixture :TestClient):
    response = client_fixture.delete("/tasks/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"