from fastapi.testclient import TestClient

def test_find_all(client_fixture :TestClient):
    response = client_fixture.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2

def test_find_by_due_正常系(client_fixture :TestClient):
    response = client_fixture.get("/items/?due_date=2025-10-30&end=7")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2

def test_find_by_due_異常系(client_fixture :TestClient):
    response = client_fixture.get("/items/?due_date=2025-11-30&end=7")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
# def test_find_by_due_fromtoday_正常系()

# def test_find_by_due_fromtoday_異常系()
    
# def test_find_by_id_正常系()
# def test_find_by_id_異常系()

# def test_create()
    
# def test_update_正常系()
# def test_update_異常系()
    
# def test_delete_正常系()
# def test_delete_異常系()