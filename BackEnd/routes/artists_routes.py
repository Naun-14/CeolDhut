from flask import Blueprint, request, jsonify
from models import db, Artist, User
import jwt
import os

artists_bp = Blueprint("artists", __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'ceoldhut key')


def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None


@artists_bp.route("", methods=["GET"])
def get_all_artists():
    """Get all artists"""
    
    artists = Artist.query.all()
    
    return jsonify({
        "artists": [
            {
                "id": a.id,
                "name": a.name,
                "country": a.country,
                "verified": a.verified,
                "spotify_id": a.spotify_id
            }
            for a in artists
        ]
    }), 200


@artists_bp.route("/verified", methods=["GET"])
def get_verified_artists():
    """Get only verified Celtic artists"""
    
    artists = Artist.query.filter_by(verified=True).all()
    
    return jsonify({
        "verified_artists": [
            {
                "id": a.id,
                "name": a.name,
                "country": a.country,
                "spotify_id": a.spotify_id
            }
            for a in artists
        ]
    }), 200


@artists_bp.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """Get a specific artist"""
    
    artist = Artist.query.filter_by(id=artist_id).first()
    
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    
    return jsonify({
        "id": artist.id,
        "name": artist.name,
        "country": artist.country,
        "verified": artist.verified,
        "spotify_id": artist.spotify_id
    }), 200


@artists_bp.route("", methods=["POST"])
def create_artist():
    """Create a new artist"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    data = request.json
    name = data.get("name")
    country = data.get("country")
    spotify_id = data.get("spotify_id")
    
    if not name:
        return jsonify({"error": "Artist name required"}), 400
    
    # Check if artist already exists
    existing = Artist.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Artist already exists"}), 400
    
    artist = Artist(
        name=name,
        country=country,
        spotify_id=spotify_id,
        verified=False
    )
    
    db.session.add(artist)
    db.session.commit()
    
    return jsonify({
        "message": "Artist created",
        "id": artist.id,
        "name": artist.name
    }), 201


@artists_bp.route("/<int:artist_id>/verify", methods=["PUT"])
def verify_artist(artist_id):
    """Verify an artist (Admin only)"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Check if user is admin
    user = User.query.filter_by(id=user_id).first()
    if not user or user.role != 'ADMIN':
        return jsonify({"error": "Admin access required"}), 403
    
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    
    artist.verified = True
    artist.verified_by = user_id
    db.session.commit()
    
    return jsonify({
        "message": "Artist verified",
        "id": artist.id,
        "name": artist.name,
        "verified": True
    }), 200


@artists_bp.route("/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id):
    """Update artist information"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Check if user is admin
    user = User.query.filter_by(id=user_id).first()
    if not user or user.role != 'ADMIN':
        return jsonify({"error": "Admin access required"}), 403
    
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    
    data = request.json
    
    if "name" in data:
        artist.name = data.get("name")
    if "country" in data:
        artist.country = data.get("country")
    if "spotify_id" in data:
        artist.spotify_id = data.get("spotify_id")
    
    db.session.commit()
    
    return jsonify({
        "message": "Artist updated",
        "id": artist.id,
        "name": artist.name
    }), 200


@artists_bp.route("/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    """Delete an artist (Admin only)"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Check if user is admin
    user = User.query.filter_by(id=user_id).first()
    if not user or user.role != 'ADMIN':
        return jsonify({"error": "Admin access required"}), 403
    
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    
    db.session.delete(artist)
    db.session.commit()
    
    return jsonify({"message": "Artist deleted"}), 200