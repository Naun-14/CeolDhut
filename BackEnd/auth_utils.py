from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from models import User


def get_secret_key():
    return current_app.config.get("SECRET_KEY", "ceoldhut key")


def get_bearer_token():
    token = request.headers.get("Authorization", "").strip()
    if not token:
        return None
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token or None


def decode_token(token):
    try:
        return jwt.decode(token, get_secret_key(), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def get_current_user():
    token = get_bearer_token()
    if not token:
        return None, ("Missing token", 401)

    payload = decode_token(token)
    if not payload:
        return None, ("Invalid token", 401)

    user = User.query.filter_by(id=payload.get("user_id")).first()
    if not user:
        return None, ("Invalid token", 401)

    return user, None


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user, error = get_current_user()
        if error:
            message, status = error
            return jsonify({"error": message}), status
        g.current_user = user
        return view(*args, **kwargs)

    return wrapped


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user, error = get_current_user()
        if error:
            message, status = error
            return jsonify({"error": message}), status
        if user.role != "ADMIN":
            return jsonify({"error": "Admin access required"}), 403
        g.current_user = user
        return view(*args, **kwargs)

    return wrapped
