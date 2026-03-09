from flask import Flask
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt
from models import db
import os

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize database and bcrypt
db.init_app(app)
bcrypt = Bcrypt(app)

# Import routes AFTER db initialization
from routes.auth_routes import auth_bp
from routes.playlist_routes import playlist_bp
from routes.tracks_routes import tracks_bp
from routes.events_routes import events_bp
from routes.artists_routes import artists_bp
from routes.music_routes import music_bp

# Register all blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(playlist_bp, url_prefix="/api/playlists")
app.register_blueprint(tracks_bp, url_prefix="/api/tracks")
app.register_blueprint(events_bp, url_prefix="/api/events")
app.register_blueprint(artists_bp, url_prefix="/api/artists")
app.register_blueprint(music_bp, url_prefix="/api/music")

@app.route("/")
def home():
    return {"message": "CeolDhut API Running"}

if __name__ == "__main__":
    app.run(debug=True)