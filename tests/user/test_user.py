
from fastapi import status
from fastapi.testclient import TestClient

# create dummy fake data
UserName = "test"
UserPassword = "<PASSWORD>"
UserEmail = "email@email.com"

user_create_data = {
    "name": UserName,
    "email": UserEmail,
    "password": UserPassword,
}


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/users/",
        json=user_create_data,
        # headers={'Authorization': f'Bearer {user_access_token}'},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "password" not in response.json()
