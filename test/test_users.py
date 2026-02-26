from fastapi import status

def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={"username": "newuser123", "password": "securepass"}
    )
    assert response.status_code == status.HTTP_200_OK  # your code returns 200, not 201
    data = response.json()
    assert data["username"] == "newuser123"
    assert "id" in data
    assert "hashed_password" not in data  # good security


def test_create_user_duplicate(client):
    # First user
    client.post("/users/", json={"username": "duplicate", "password": "pass"})
    
    # Second attempt
    response = client.post("/users/", json={"username": "duplicate", "password": "pass"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username taken" in response.json()["detail"]


def test_create_user_missing_field(client):
    response = client.post("/users/", json={"username": "no_pass"})
    assert response.status_code == 422  # Pydantic validation error