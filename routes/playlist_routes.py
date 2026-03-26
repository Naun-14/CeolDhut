from flask import Blueprint, request, jsonify
from models import db, Playlist
import jwt
import os

playlist_bp = Blueprint("playlists", __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'ceoldhut key')


def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None


@playlist_bp.route("", methods=["GET"])
def get_playlists():
    """Get all playlists for logged-in user"""
    
    # Get token from header
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    # Remove "Bearer " prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    # Verify token
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Get user's playlists
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "playlists": [
            {
                "id": p.id,
                "name": p.name,
                "created_at": p.created_at.isoformat()
            }
            for p in playlists
        ]
    }), 200


@playlist_bp.route("", methods=["POST"])
def create_playlist():
    """Create a new playlist"""
    
    # Get token
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    # Verify token
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Get data
    data = request.json
    name = data.get("name")
    
    if not name:
        return jsonify({"error": "Playlist name required"}), 400
    
    # Create playlist
    new_playlist = Playlist(
        user_id=user_id,
        name=name
    )
    
    db.session.add(new_playlist)
    db.session.commit()
    
    return jsonify({
        "message": "Playlist created",
        "id": new_playlist.id,
        "name": new_playlist.name
    }), 201


@playlist_bp.route("/<int:playlist_id>", methods=["PUT"])
def update_playlist(playlist_id):
    """Update playlist name"""
    
    # Get token
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Find playlist
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
    
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    
    # Update name
    data = request.json
    name = data.get("name")
    
    if name:
        playlist.name = name
        db.session.commit()
    
    return jsonify({
        "message": "Playlist updated",
        "id": playlist.id,
        "name": playlist.name
    }), 200


@playlist_bp.route("/<int:playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    """Delete a playlist"""
    
    # Get token
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Find playlist
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
    
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    
    # Delete
    db.session.delete(playlist)
    db.session.commit()
    
    return jsonify({"message": "Playlist deleted"}), 200