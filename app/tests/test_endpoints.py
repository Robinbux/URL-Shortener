import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import crud
from ..api.endpoints import get_db
from ..database import Base
from ..main import app
from ..utils import generate_shortcode

from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


def test_create_short_url(client):
    test_url = "https://test.com"
    response = client.post("/shorten", json={"url": test_url})
    assert response.status_code == 201
    assert "shortcode" in response.json()
    shortcode = response.json()["shortcode"]

    # Test for already shortened URL
    response = client.post("/shorten", json={"url": test_url}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers.get("Location") == f"/urls/{shortcode}"


def test_redirect_to_original(client, test_db):
    test_url = "https://example.com"
    shortcode = generate_shortcode()
    crud.create_short_url(test_db, original_url=test_url, shortcode=shortcode)
    test_db.commit()

    response = client.get(f"/urls/{shortcode}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers.get("location") == test_url


def test_get_statistics(client, test_db):
    test_url = "https://example.com/"
    shortcode = generate_shortcode()
    crud.create_short_url(test_db, original_url=test_url, shortcode=shortcode)
    test_db.commit()

    response = client.get(f"/urls/{shortcode}/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["url"] == test_url
    assert stats["hits"] == 0


def test_hit_update(client, test_db):
    test_url = "https://example.com/"
    shortcode = generate_shortcode()
    crud.create_short_url(test_db, original_url=test_url, shortcode=shortcode)
    test_db.commit()

    for _ in range(5):
        response = client.get(f"/urls/{shortcode}", follow_redirects=False)
        assert response.status_code == 307

    response = client.get(f"/urls/{shortcode}/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["hits"] == 5


def test_404_for_invalid_shortcode(client):
    response = client.get("/urls/invalid_shortcode")
    assert response.status_code == 404

    response = client.get("/urls/invalid_shortcode/stats")
    assert response.status_code == 404
