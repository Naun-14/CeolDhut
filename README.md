# CeolDhut

CeolDhut is a full-stack music platform with a Flask backend, a public listener experience, an admin workspace, playlist and event features, and Spotify-powered search.

## Structure

- `BackEnd/` Flask app, models, config, and API routes
- `ceoldhut-frontend/` integrated frontend served by Flask

## Core Features

- authentication with JWT
- user and admin flows
- playlists, tracks, artists, and events
- Spotify search integration

## Local Run

Install dependencies:

```bash
pip install -r BackEnd/requirements.txt
```

Set environment variables:

- `DATABASE_URL`
- `SECRET_KEY`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`

Run locally:

```bash
python BackEnd/app.py
```


## Main Routes

- `/`
- `/login`
- `/music`
- `/artists`
- `/events`
- `/account`
- `/admin`
- `/api/auth/*`
- `/api/artists/*`
- `/api/tracks/*`
- `/api/playlists/*`
- `/api/events/*`
- `/api/music/*`

