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

## Production Start Command

Use Gunicorn from the `BackEnd` folder:

```bash
gunicorn --chdir BackEnd wsgi:app
```

## Suggested Deployment Order

1. Put the code in GitHub.
2. Create a hosted MySQL database.
3. Add the environment variables in your hosting platform.
4. Deploy the Flask app with:

```bash
gunicorn --chdir BackEnd wsgi:app
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

