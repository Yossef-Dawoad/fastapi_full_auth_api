from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from auth.confdb import Base, get_db
from auth.confemail import fm
from auth.user.models import User
from main import app

# create a test database connection
engine = create_engine("sqlite:///./test.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
def test_dbsession() -> Generator:
    session = SessionTesting()
    try: yield session
    finally: session.close()

@pytest.fixture(scope="function")
def app_test() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(app_test, test_dbsession) -> Generator:   # noqa: ANN001
    def _test_db():  # noqa: ANN202
        try: yield test_dbsession
        finally: pass
    app_test.dependency_overrides[get_db] = _test_db
    fm.config.SUPPRESS_SEND = 1 # dont send in test env
    return TestClient(app_test)

@pytest.fixture(scope="function")
def inactive_user(test_dbsession: Session) -> User:
    user = User(
        **user_create_data,
        is_active=False,
        updated_at=datetime.now(timezone.utc),
    )

    test_dbsession.add(user)
    test_dbsession.commit()
    test_dbsession.refresh(user)
    return user
