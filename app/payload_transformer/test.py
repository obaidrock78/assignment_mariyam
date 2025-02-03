from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_read_payload():
    # Test payload creation
    response = client.post(
        "/payload", json={"list_1": ["test1", "test2"], "list_2": ["test3", "test4"]}
    )
    assert response.status_code == 200
    payload_id = response.json()["id"]

    # Test reading the payload
    get_response = client.get(f"/payload/{payload_id}")
    assert get_response.status_code == 200
    assert get_response.json()["output"] == "TEST1, TEST3, TEST2, TEST4"


def test_duplicate_payload():
    # Create first payload
    response1 = client.post(
        "/payload", json={"list_1": ["a", "b"], "list_2": ["c", "d"]}
    )
    assert response1.status_code == 200
    payload_id = response1.json()["id"]

    # Create duplicate payload
    response2 = client.post(
        "/payload", json={"list_1": ["a", "b"], "list_2": ["c", "d"]}
    )
    assert response2.status_code == 200
    assert response2.json()["id"] == payload_id


def test_invalid_lists_length():
    response = client.post("/payload", json={"list_1": ["a", "b"], "list_2": ["c"]})
    assert response.status_code == 400
