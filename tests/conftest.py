import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.utils.database import Base
from app.config import TESTING_DATABASE_URI
from app.main import app


@pytest.fixture(scope="module")
def test_app():
    app.dependency_overrides[get_database] = get_test_database
    yield TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(TESTING_DATABASE_URI)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def get_test_database():
    engine = create_engine(TESTING_DATABASE_URI)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
