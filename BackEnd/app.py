from flask import Flask
from config import Config
from routes.auth_routes import auth_bp
from models.user import db

app = Flask(__name__)
app.config.from_object(Config)

# connect SQLAlchemy to Flask
db.init_app(app)

# register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"message": "CeolDhut API Running"}

if __name__ == "__main__":
    app.run(debug=True)