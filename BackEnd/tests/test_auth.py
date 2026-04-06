from conftest import login_user, register_user


def test_register_creates_standard_user(client, app):
    response = register_user(client, email="newuser@example.com", password="password123")

    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

    with app.app_context():
        from models import User

        user = User.query.filter_by(email="newuser@example.com").first()
        assert user is not None
        assert user.role == "USER"


def test_register_rejects_duplicate_email(client):
    register_user(client)
    response = register_user(client)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already registered"


def test_register_validates_email_and_password(client):
    invalid_email = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "password123"},
    )
    short_password = client.post(
        "/api/auth/register",
        json={"email": "short@example.com", "password": "123"},
    )

    assert invalid_email.status_code == 400
    assert invalid_email.get_json()["error"] == "Invalid email format"
    assert short_password.status_code == 400
    assert short_password.get_json()["error"] == "Password must be at least 6 characters"


def test_register_cannot_escalate_to_admin(client, app):
    response = client.post(
        "/api/auth/register",
        json={"email": "admintry@example.com", "password": "password123", "role": "ADMIN"},
    )

    assert response.status_code == 201

    with app.app_context():
        from models import User

        user = User.query.filter_by(email="admintry@example.com").first()
        assert user.role == "USER"


def test_login_returns_token_and_role(client):
    register_user(client, email="login@example.com", password="password123")
    response = login_user(client, email="login@example.com", password="password123")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["token"]
    assert payload["role"] == "USER"


def test_login_rejects_bad_password(client):
    register_user(client, email="loginfail@example.com", password="password123")
    response = login_user(client, email="loginfail@example.com", password="wrongpassword")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"
