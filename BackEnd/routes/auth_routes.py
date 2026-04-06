from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

SECRET_KEY = os.getenv('SECRET_KEY', 'ceoldhut key')
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_role = data.get("role")

            if user_role != "ADMIN":
                return jsonify({"error": "Admin access required"}), 403

        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user"""

    data = request.json

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    email = data.get("email")
    password = data.get("password")
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        email=email,
        password_hash=password_hash,
        role="USER"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in a user and return JWT token"""

    data = request.json

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }), 200
