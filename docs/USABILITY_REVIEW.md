# Usability Review

## Scope

This review focused on the most important end-to-end flows in the application:

- new user registration and login
- browsing music and searching Spotify-backed content
- creating and managing playlists
- accessing the admin dashboard
- using the deployed app across desktop and mobile browsers

## Review Method

A structured scenario-based review was carried out against the deployed application and local development environment. The goal was to identify blockers, confusing interactions, and issues that would interrupt a normal user journey.

## Scenarios Reviewed

### 1. New user onboarding

Task:

- open the app
- create an account
- log in
- reach the correct dashboard

Outcome:

- the flow works after deployment fixes
- role escalation during public signup was removed

Changes made:

- public registration now always creates `USER` accounts
- deployment database setup was corrected so registration works reliably

### 2. Music discovery and search

Task:

- open the music page
- browse featured content
- search for tracks and artists

Outcome:

- featured content and search now work through the backend Spotify routes
- search rendering is more stable than earlier project versions

Changes made:

- frontend search rendering was hardened
- Spotify search limits were aligned with the backend behavior
- deployed API base path was corrected for non-local devices

### 3. Playlist workflow

Task:

- create a playlist
- add a track
- avoid duplicate additions

Outcome:

- the workflow is available to logged-in users
- duplicate additions are blocked

Changes made:

- playlist validation was tightened on the backend
- track creation checks now reject invalid artist references

### 4. Admin workflow

Task:

- access admin-only features
- create artists and events
- inspect registrations

Outcome:

- admin-only routes are protected by backend checks
- admin privileges must now come from the database, not public signup

Changes made:

- admin-only protection was unified across routes
- public admin registration was removed

### 5. Cross-device access

Task:

- open the deployed app on devices other than the development PC
- log in and use the main flows

Outcome:

- deployment issues initially blocked backend-driven features on non-local devices
- those issues were traced to incorrect API base routing and deployment configuration

Changes made:

- deployed frontend now uses same-origin `/api`
- production configuration strips whitespace from env values
- Aiven SSL options are applied automatically in backend configuration

## Main Findings

### Strengths

- clear split between client and admin areas
- straightforward navigation for core pages
- simple account and playlist flow
- meaningful external API integration through Spotify

### Weaknesses Found During Review

- deployment was initially fragile because database and environment configuration were incomplete
- some frontend code paths depended on newer browser syntax that reduced resilience
- early versions allowed unsafe public admin account creation
- documentation and test coverage were below the level expected for a polished submission

## Actions Taken

- added backend unit tests
- improved backend validation and auth handling
- strengthened deployment configuration
- improved README and API documentation
- documented the testing and review process in the repository
