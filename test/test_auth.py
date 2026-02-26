from fastapi import status

def test_login_success(client):
    # First create user
    client.post("/users/", json={"username": "logintest", "password": "correctpass"})

    response = client.post(
        "/token",
        data={"username": "logintest", "password": "correctpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/users/", json={"username": "wrongpassuser", "password": "rightpass"})
    
    response = client.post(
        "/token",
        data={"username": "wrongpassuser", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in response.json()["detail"]


def test_login_nonexistent_user(client):
    response = client.post(
        "/token",
        data={"username": "doesnotexist", "password": "anything"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in response.json()["detail"]