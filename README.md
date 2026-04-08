# CeolDhut

CeolDhut is a full-stack music discovery platform built around Celtic music, artists, playlists, and live events. The project includes a Flask backend API, a listener-facing frontend, an admin workspace, and Spotify integration for music search.

## Live Application

- Production app: `https://ceoldhut.onrender.com/`
- Health check: `https://ceoldhut.onrender.com/api/health`

## Core Features

- JWT authentication and role-based access control
- Public client experience for music discovery, playlists, artists, and events
- Admin workspace for managing artists and events
- Spotify-powered search for tracks, artists, and playlists
- Playlist management with add/remove track flows
- Event registration for logged-in users

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Flask, Flask-SQLAlchemy, Flask-Bcrypt
- Database: MySQL
- External API: Spotify Web API via Spotipy
- Deployment: Render + Aiven MySQL
- Testing: Pytest

## Project Structure

- `BackEnd/`
  Flask application, models, configuration, and API routes
- `ceoldhut-frontend/`
  Frontend pages, styling, and browser-side scripts
- `BackEnd/tests/`
  Backend unit tests
- `docs/`
  API documentation, testing notes, and usability review

## User Roles

- `USER`
  Can register, log in, browse music, manage playlists, and register for events
- `ADMIN`
  Can access the admin dashboard and manage artists and events

Admin users are created by promoting a user record in the database. Public registration always creates a standard `USER` account.

## Local Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Application dependencies:

```bash
pip install -r BackEnd/requirements.txt
```

Test dependencies:

```bash
pip install -r BackEnd/requirements-dev.txt
```

### 5. Run the app

```bash
python BackEnd/app.py
```

The app will be available at:

- https://ceoldhut.onrender.com (Will take time to load as the service we are hosting isnt free)

## Deployment

Production deployment uses:

- Render for the Flask web service
- Aiven for the hosted MySQL database

Start command:

```bash
gunicorn --chdir BackEnd wsgi:app
```

The backend configuration trims environment-variable whitespace automatically and enables SSL engine options when using an Aiven MySQL connection string.

## Testing

Run the backend unit tests with:

```bash
python -m pytest
```

Current automated coverage includes:

- authentication and login
- registration validation
- prevention of public admin escalation
- playlist creation and duplicate handling
- track addition and duplicate prevention
- admin-only route protection
- event creation and event registration flow

Latest local test result:

- `14 passed`

More detail is available in [TESTING.md](/C:/Users/abdul/Documents/CeolDhut/docs/TESTING.md). (Refer to DOCS folder)

## API Documentation

Two forms of API documentation are included:

- human-readable reference: [API_REFERENCE.md](/C:/Users/abdul/Documents/CeolDhut/docs/API_REFERENCE.md)  (Refer to DOCS folder)
- OpenAPI specification: [openapi.yaml](/C:/Users/abdul/Documents/CeolDhut/docs/openapi.yaml)  (Refer to DOCS folder)

## Main Application Routes

- `/`
- `/login`
- `/account`
- `/music`
- `/artists`
- `/events`
- `/admin`

## Main API Route Groups

- `/api/auth/*`
- `/api/playlists/*`
- `/api/tracks/*`
- `/api/artists/*`
- `/api/events/*`
- `/api/music/*`

## Security Notes

- passwords are hashed with Bcrypt
- JWT tokens are used for authenticated routes
- public signup creates only standard users
- admin-only actions are protected on the backend
- production secrets are loaded from environment variables
- database and secret environment values are stripped to avoid whitespace-related deployment failures

## Usability Review

A structured usability review for the current UI and core user flows is documented in [USABILITY_REVIEW.md](/C:/Users/abdul/Documents/CeolDhut/docs/USABILITY_REVIEW.md).  (Refer to DOCS folder)


**Installation**

1. Clone or download the repository
Using Git:

git clone https://github.com/Naun-14/CeolDhut.git
cd CeolDhut
Or download the ZIP from GitHub, extract it, and open the project folder in PowerShell.

2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
If PowerShell blocks activation, run:

Set-ExecutionPolicy -Scope Process Bypass

3. Install dependencies
Application dependencies:

pip install -r BackEnd\requirements.txt
Optional test dependencies:

pip install -r BackEnd\requirements-dev.txt

4. Configure environment variables
Create a .env file inside BackEnd using BackEnd/.env.example as a template.

Required values:

DATABASE_URL=mysql+pymysql://username:password@host:3306/database_name
SECRET_KEY=replace-with-a-long-random-secret
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret


5. Create database tables
If the database is empty, run:

cd BackEnd
..\venv\Scripts\python.exe -c "from app import app; from models import db; app.app_context().push(); db.create_all(); print('tables created')"
cd ..
6. Run the application
python BackEnd\app.py
7. Open the app
Go to:
http://127.0.0.1:5000/

