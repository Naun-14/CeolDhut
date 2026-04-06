import re
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, jsonify, request
from flask_bcrypt import Bcrypt
from models import db, User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"error": "Invalid email format"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

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
    data = request.get_json(silent=True) or {}

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    email = data.get("email").strip().lower()
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
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }), 200
