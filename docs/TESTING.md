# Testing

## Automated Backend Tests

Backend unit tests are located in `BackEnd/tests/` and run with `pytest`.

Run them with:

```bash
python -m pytest
```

Latest local result:

```text
14 passed
```

## Covered Flows

### Authentication

- register a new user successfully
- reject duplicate email registration
- reject invalid email format
- reject short passwords
- prevent public registration from creating admin users
- log in successfully and return a JWT
- reject invalid login credentials

### Playlists and Tracks

- block playlist creation without a token
- create, list, update, and delete playlists
- block duplicate playlist names for the same user
- add tracks to playlists
- block duplicate track additions
- reject track creation when the referenced artist does not exist

### Admin and Events

- block artist creation for non-admin users
- allow artist creation for admin users
- block event creation for non-admin users
- allow admin event creation
- allow user event registration
- block duplicate registration for the same event
- allow admins to view event registrations

## Manual Smoke Testing

The following manual checks were used alongside the unit tests:

- deployed health endpoint returns `200`
- account registration works against the hosted database
- login persists into frontend role-aware navigation
- music search works through Spotify integration
- playlist add/remove flows work for logged-in users
- admin dashboard is accessible only to admin users

## Remaining Gaps

- no frontend browser automation is included yet
- music route tests currently depend on live Spotify credentials, so Spotify endpoints were not unit tested in the automated suite
- usability evidence is documented separately in [USABILITY_REVIEW.md](/C:/Users/abdul/Documents/CeolDhut/docs/USABILITY_REVIEW.md)
