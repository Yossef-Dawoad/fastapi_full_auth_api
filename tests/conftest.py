from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.confdb import Base, get_db
from main import app

# create a test database connection
engine = create_engine("sqlite:///./test.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)




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
    return TestClient(app_test)
