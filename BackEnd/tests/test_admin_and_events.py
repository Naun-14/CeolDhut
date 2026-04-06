def test_artist_creation_requires_admin(client, user_token):
    response = client.post(
        "/api/artists",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Test Artist"},
    )

    assert response.status_code == 403
    assert response.get_json()["error"] == "Admin access required"


def test_admin_can_create_artist(client, admin_token):
    response = client.post(
        "/api/artists",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Test Artist", "country": "Scotland"},
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "Test Artist"


def test_event_creation_requires_admin(client, user_token):
    response = client.post(
        "/api/events",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Session Night"},
    )

    assert response.status_code == 403
    assert response.get_json()["error"] == "Admin access required"


def test_admin_event_flow_and_user_registration(client, admin_token, user_token):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    create_event = client.post(
        "/api/events",
        headers=admin_headers,
        json={
            "title": "Session Night",
            "location": "Dundee",
            "event_date": "2026-05-01T19:30:00",
            "description": "Live traditional set",
        },
    )
    event_id = create_event.get_json()["id"]

    first_register = client.post(
        f"/api/events/{event_id}/register",
        headers=user_headers,
    )
    second_register = client.post(
        f"/api/events/{event_id}/register",
        headers=user_headers,
    )
    registrations = client.get(
        f"/api/events/{event_id}/registrations",
        headers=admin_headers,
    )

    assert create_event.status_code == 201
    assert first_register.status_code == 201
    assert second_register.status_code == 400
    assert second_register.get_json()["error"] == "Already registered for this event"
    assert registrations.status_code == 200
    assert len(registrations.get_json()["registrations"]) == 1
