
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from auth.user.models import User

# create dummy fake data
UserName = "test"
UserPassword = "<Password123>"
UserEmail = "keshari@describly.com"

user_create_data = {
    "name": UserName,
    "email": UserEmail,
    "password": UserPassword,
}


@pytest.fixture(scope="function")
def inactive_user(test_dbsession: Session) -> User:
    user = User(**user_create_data, is_active=False)

    test_dbsession.add(user)
    test_dbsession.commit()
    test_dbsession.refresh(user)
    return user


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/users/",
        json=user_create_data,
    )
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert "password" not in response.json()


def test_create_user_with_existing_email(client: TestClient, inactive_user: User) -> None:
    user_create_data["email"] = inactive_user.email

    response = client.post("/users/", json=user_create_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_with_invalid_email(client: TestClient) -> None:

    user_create_data["email"] = "joe.com"
    response = client.post("/users/", json=user_create_data)

    err_message = 'value is not a valid email address: The email address' \
                  ' is not valid. It must have exactly one @-sign.'

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == err_message

def test_create_user_with_empty_password(client: TestClient) -> None:
    user_create_data["email"] = "keshari@describly.com"
    user_create_data["password"] = ""
    response = client.post("/users/", json=user_create_data)

    err_message = 'String should have at least 8 characters'

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]['msg'] == err_message

def test_create_user_with_numeric_password(client: TestClient) -> None:

    user_create_data["password"] = "1232382318763"
    response = client.post("/users/", json=user_create_data)

    err_message = "try compination of Upper and digit " \
                "with special chracters in your password"

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == err_message


def test_create_user_with_char_password(client: TestClient) -> None:

    user_create_data["password"] = "asjhgahAdF"
    response = client.post("/users/", json=user_create_data)

    err_message = "try compination of Upper and digit " \
                "with special chracters in your password"

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == err_message


def test_create_user_with_alphanumeric_password(client: TestClient) -> None:

    user_create_data["password"] = "sjdgajhGG27862"
    response = client.post("/users/", json=user_create_data)

    err_message = "try compination of Upper and digit " \
                "with special chracters in your password"

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == err_message
