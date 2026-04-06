from flask import Flask, send_from_directory
from config import Config
from flask_bcrypt import Bcrypt
from models import db
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_FRONTEND_DIR = os.path.join(PROJECT_ROOT, "ceoldhut-frontend")
LEGACY_FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
FRONTEND_DIR = DEFAULT_FRONTEND_DIR if os.path.isdir(DEFAULT_FRONTEND_DIR) else LEGACY_FRONTEND_DIR

bcrypt = Bcrypt()


def create_app(config_overrides=None):
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    bcrypt.init_app(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    from routes.auth_routes import auth_bp
    from routes.playlist_routes import playlist_bp
    from routes.tracks_routes import tracks_bp
    from routes.events_routes import events_bp
    from routes.artists_routes import artists_bp
    from routes.music_routes import music_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(playlist_bp, url_prefix="/api/playlists")
    app.register_blueprint(tracks_bp, url_prefix="/api/tracks")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(artists_bp, url_prefix="/api/artists")
    app.register_blueprint(music_bp, url_prefix="/api/music")

    @app.route("/")
    def home():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/client")
    def client_app():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/admin")
    def admin_app():
        return send_from_directory(FRONTEND_DIR, "admin.html")

    @app.route("/login")
    def login_page():
        return send_from_directory(FRONTEND_DIR, "login.html")

    @app.route("/account")
    def account_page():
        return send_from_directory(FRONTEND_DIR, "account.html")

    @app.route("/music")
    def music_page():
        return send_from_directory(FRONTEND_DIR, "music.html")

    @app.route("/artists")
    def artists_page():
        return send_from_directory(FRONTEND_DIR, "artists.html")

    @app.route("/events")
    def events_page():
        return send_from_directory(FRONTEND_DIR, "events.html")

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {
            "status": "ok",
            "message": "API is running"
        }, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    )
