from conftest import register_user


def test_create_playlist_requires_auth(client):
    response = client.post("/api/playlists", json={"name": "Roadtrip"})

    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing token"


def test_playlist_crud_flow(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    create_response = client.post("/api/playlists", headers=headers, json={"name": "Roadtrip"})
    playlist = create_response.get_json()
    playlist_id = playlist["id"]

    duplicate_response = client.post("/api/playlists", headers=headers, json={"name": "Roadtrip"})
    list_response = client.get("/api/playlists", headers=headers)
    update_response = client.put(
        f"/api/playlists/{playlist_id}",
        headers=headers,
        json={"name": "Late Night"},
    )
    delete_response = client.delete(f"/api/playlists/{playlist_id}", headers=headers)

    assert create_response.status_code == 201
    assert duplicate_response.status_code == 400
    assert list_response.status_code == 200
    assert len(list_response.get_json()["playlists"]) == 1
    assert update_response.status_code == 200
    assert update_response.get_json()["name"] == "Late Night"
    assert delete_response.status_code == 200


def test_add_track_to_playlist_blocks_duplicates(client, user_token, playlist, track):
    headers = {"Authorization": f"Bearer {user_token}"}

    first_add = client.post(
        f"/api/tracks/playlist/{playlist.id}/tracks",
        headers=headers,
        json={"track_id": track.id},
    )
    second_add = client.post(
        f"/api/tracks/playlist/{playlist.id}/tracks",
        headers=headers,
        json={"track_id": track.id},
    )

    assert first_add.status_code == 201
    assert second_add.status_code == 400
    assert second_add.get_json()["error"] == "Track already in playlist"


def test_create_track_requires_existing_artist(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post(
        "/api/tracks",
        headers=headers,
        json={"title": "Ghost Song", "artist_id": 9999},
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Artist not found"
