"""
1. User should be able to login
2. User should not be able to login with incorrect password
3. Inactive user should not be able to login.
4. Unverified user should not be able to login.
.....
"""
from fastapi import status
from fastapi.testclient import TestClient

from auth.user.models import User


def test_user_login(client: TestClient, user: User) -> None:
    response = client.post(
        '/api/v1/users/login',
        data={'username':user.email, 'password':user.password},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['access_token'] is not None
    assert response.json()['token_type'] == 'bearer'

def test_user_login_with_incorrect_password(client: TestClient, user: User) -> None:
    response = client.post(
        '/api/v1/users/login',
        data={'username':user.email, 'password':'<PASSWORD>'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect username or password'

def test_user_login_with_inactive_user(client: TestClient, inactive_user: User) -> None:

    response = client.post(
        '/api/v1/users/login',
        data={'username':inactive_user.email, 'password':inactive_user.password},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Inactive user'

def test_user_login_with_unverified_user(client: TestClient, unverified_user: User) -> None:
    pass
