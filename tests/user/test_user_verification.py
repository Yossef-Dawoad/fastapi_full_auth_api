

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from auth.user.email import VERIFY_ACCOUNT_CTX
from auth.user.models import User
from auth.user.security import get_str_hash


def test_user_acc_verification(client:TestClient, inactive_user: User, test_dbsession: Session) -> None:
    user_token = inactive_user.user_ctx_token(context=VERIFY_ACCOUNT_CTX)
    token_hash = get_str_hash(user_token)
    data = {
        'email': inactive_user.email,
        'token': token_hash,
    }
    response = client.post(
        '/users/verify-account',
        json=data,
        headers={'Content-Type': 'application/json'},
    )
    print(response.json())
    activated_user = test_dbsession.query(User).filter(User.email == inactive_user.email).first()
    assert response.status_code == status.HTTP_200_OK
    assert activated_user.is_active is True
    assert activated_user.verified_at is not None


def test_user_activated_with_invalid_token(client:TestClient, inactive_user: User) -> None:

    data = {
        'email': inactive_user.email,
        'token': '$argon2id$v=19$m=65536,t=3,p=4$s1aK8b43phTinHMOYQyBsA$yNeogWxULhlEVHAr+bW0fSMet3FL5BkS5TmaLmQu5i4',

    }
    response = client.post(
        '/users/verify-account',
        json=data,
        headers={'Content-Type': 'application/json'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Invalid Token'

def test_user_invalid_email_does_not_work(
        client:TestClient,
        inactive_user:User,
        test_dbsession:Session,
    ) -> None:
    user_token = inactive_user.user_ctx_token(VERIFY_ACCOUNT_CTX)
    token_hash = get_str_hash(user_token)
    data = {
        "email": "nandan@describly.com",
        "token": token_hash,
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != status.HTTP_200_OK
    activated_user = test_dbsession.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is False
    assert activated_user.verified_at is None
