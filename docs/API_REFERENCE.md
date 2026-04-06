# API Reference

Base URL in production:

```text
https://ceoldhut.onrender.com/api
```

Authentication uses a Bearer token in the `Authorization` header:

```text
Authorization: Bearer <jwt>
```

## Auth

### `POST /auth/register`

Creates a standard user account.

Request body:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### `POST /auth/login`

Logs a user in and returns a JWT token plus role information.

Request body:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

## Playlists

### `GET /playlists`

Returns the logged-in user’s playlists.

### `POST /playlists`

Creates a playlist for the logged-in user.

Request body:

```json
{
  "name": "Roadtrip"
}
```

### `PUT /playlists/{playlist_id}`

Renames a playlist owned by the logged-in user.

### `DELETE /playlists/{playlist_id}`

Deletes a playlist owned by the logged-in user.

## Tracks

### `GET /tracks/playlist/{playlist_id}/tracks`

Returns tracks in a playlist owned by the logged-in user.

### `POST /tracks/playlist/{playlist_id}/tracks`

Adds an existing track to a playlist.

Request body:

```json
{
  "track_id": 1
}
```

### `DELETE /tracks/playlist/{playlist_id}/tracks/{track_id}`

Removes a track from a playlist.

### `POST /tracks`

Creates a track record for playlist usage or admin data management.

Request body:

```json
{
  "title": "The Rocky Road",
  "artist_id": 1,
  "spotify_id": "spotify-track-id",
  "duration_ms": 180000
}
```

## Artists

### `GET /artists`

Returns all artists.

### `GET /artists/verified`

Returns only verified artists.

### `GET /artists/{artist_id}`

Returns one artist by ID.

### `POST /artists`

Admin-only. Creates an artist.

### `PUT /artists/{artist_id}`

Admin-only. Updates an artist.

### `PUT /artists/{artist_id}/verify`

Admin-only. Marks an artist as verified.

### `DELETE /artists/{artist_id}`

Admin-only. Deletes an artist.

## Events

### `GET /events`

Returns all events.

### `GET /events/{event_id}`

Returns one event by ID.

### `POST /events`

Admin-only. Creates an event.

Request body:

```json
{
  "title": "Session Night",
  "location": "Dundee",
  "event_date": "2026-05-01T19:30:00",
  "description": "Live traditional set"
}
```

### `PUT /events/{event_id}`

Admin-only. Updates an event.

### `DELETE /events/{event_id}`

Admin-only. Deletes an event.

### `POST /events/{event_id}/register`

Registers the logged-in user for an event.

### `DELETE /events/{event_id}/register`

Unregisters the logged-in user from an event.

### `GET /events/{event_id}/registrations`

Admin-only. Lists user registrations for an event.

## Spotify / Music

### `GET /music/search`

Searches Spotify-backed content.

Query parameters:

- `q`
- `type` = `track`, `artist`, or `playlist`
- `limit` = `1-10`

Example:

```text
/music/search?q=lankum&type=track&limit=10
```

### `GET /music/search/celtic`

Returns featured Celtic tracks.

### `GET /music/artist/{artist_id}`

Returns Spotify artist details.

### `GET /music/track/{track_id}`

Returns Spotify track details.

## Health

### `GET /health`

Simple health-check route.
