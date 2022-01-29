import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from pytest import fixture

from app.database import Base
from app.main import app, get_db


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@fixture
def faker():
    return Faker()


@fixture
def data(faker):
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "position": "SG",
        "jersey_number": faker.pyint(),
    }
    return data


def test_create_players(test_db, data):
    response = client.post("/players", json=data)
    assert response.status_code == 201
    created = response.json()


def test_get_players(test_db):
    response = client.get("/players")
    assert response.status_code == 200
    assert response.json() == []


def test_get_player_by_id(test_db, data):
    response = client.post("/players", json=data)
    assert response.status_code == 201
    created = response.json()

    response = client.get("/players/{}".format(created["id"]))
    assert response.status_code == 200
    assert response.json() == created
