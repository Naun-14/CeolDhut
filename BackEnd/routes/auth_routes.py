from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models.user import db, User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    # check if user already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # hash password
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # create user
    new_user = User(
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201