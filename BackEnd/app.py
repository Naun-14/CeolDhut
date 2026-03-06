from flask import Flask
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt
from models import db
import os

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS with specific settings
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database and bcrypt
db.init_app(app)
bcrypt = Bcrypt(app)

# Import routes AFTER db initialization
from routes.auth_routes import auth_bp
from routes.playlist_routes import playlist_bp

# Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(playlist_bp, url_prefix="/api/playlists")

@app.route("/")
def home():
    return {"message": "CeolDhut API Running"}

if __name__ == "__main__":
    app.run(debug=True)