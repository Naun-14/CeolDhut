import os
import sys
import tempfile
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import bcrypt, create_app
from models import Artist, Event, Playlist, Track, User, db


@pytest.fixture
def app():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{path}",
            "SQLALCHEMY_ENGINE_OPTIONS": {},
            "SECRET_KEY": "test-secret-key-for-suite-1234567890",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def client(app):
    return app.test_client()


def register_user(client, email="user@example.com", password="password123"):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )


def login_user(client, email="user@example.com", password="password123"):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )


@pytest.fixture
def user_token(client):
    register_user(client)
    response = login_user(client)
    return response.get_json()["token"]


@pytest.fixture
def admin_token(app, client):
    register_user(client, email="admin@example.com", password="password123")
    with app.app_context():
        admin = User.query.filter_by(email="admin@example.com").first()
        admin.role = "ADMIN"
        db.session.commit()
    response = login_user(client, email="admin@example.com", password="password123")
    return response.get_json()["token"]


@pytest.fixture
def artist(app):
    with app.app_context():
        record = Artist(name="Lankum", country="Ireland", verified=True)
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)
        return record


@pytest.fixture
def event(app):
    with app.app_context():
        record = Event(title="Celtic Night", location="Dundee")
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)
        return record


@pytest.fixture
def playlist(app, user_token, client):
    response = client.post(
        "/api/playlists",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Roadtrip"},
    )
    playlist_id = response.get_json()["id"]
    with app.app_context():
        return db.session.get(Playlist, playlist_id)


@pytest.fixture
def track(app, artist):
    with app.app_context():
        record = Track(title="The Rocky Road", artist_id=artist.id, duration_ms=180000)
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)
        return record
