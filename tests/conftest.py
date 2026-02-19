import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db
from app import models

# StaticPool forces SQLAlchemy to reuse the same in-memory connection
# so tables created by create_all are visible to all sessions.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    """TestClient with the DB dependency overridden to use the test DB."""
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def register(client, email="user@test.com", password="pass123",
             name="Test User", gender="female", age=25):
    return client.post("/auth/register", json={
        "email": email, "password": password,
        "name": name, "gender": gender, "age": age,
    })


def login(client, email="user@test.com", password="pass123"):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    return resp.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def seed_candidate(db, name="Alice", gender="female", age=26,
                   location="SF", bio="Hi", tags="hiking,coffee", photo_url=None):
    c = models.Candidate(
        name=name, gender=gender, age=age,
        location=location, bio=bio, tags=tags, photo_url=photo_url,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c
