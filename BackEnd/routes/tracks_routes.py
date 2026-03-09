from flask import Blueprint, request, jsonify
from models import db, Track, Playlist, PlaylistTrack, Artist
import jwt
import os

tracks_bp = Blueprint("tracks", __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'ceoldhut key')


def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None


@tracks_bp.route("/playlist/<int:playlist_id>/tracks", methods=["GET"])
def get_playlist_tracks(playlist_id):
    """Get all tracks in a playlist"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Verify user owns this playlist
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    
    # Get tracks in playlist
    playlist_tracks = db.session.query(Track, PlaylistTrack).join(
        PlaylistTrack, Track.id == PlaylistTrack.track_id
    ).filter(PlaylistTrack.playlist_id == playlist_id).all()
    
    tracks = [
        {
            "id": track.id,
            "title": track.title,
            "spotify_id": track.spotify_id,
            "duration_ms": track.duration_ms,
            "artist": track.artist.name if track.artist_id else "Unknown"
        }
        for track, _ in playlist_tracks
    ]
    
    return jsonify({"tracks": tracks}), 200


@tracks_bp.route("/playlist/<int:playlist_id>/tracks", methods=["POST"])
def add_track_to_playlist(playlist_id):
    """Add a track to a playlist"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Verify user owns this playlist
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    
    data = request.json
    track_id = data.get("track_id")
    
    if not track_id:
        return jsonify({"error": "Track ID required"}), 400
    
    # Check if track exists
    track = Track.query.filter_by(id=track_id).first()
    if not track:
        return jsonify({"error": "Track not found"}), 404
    
    # Check if already in playlist
    existing = PlaylistTrack.query.filter_by(
        playlist_id=playlist_id,
        track_id=track_id
    ).first()
    
    if existing:
        return jsonify({"error": "Track already in playlist"}), 400
    
    # Add track to playlist
    playlist_track = PlaylistTrack(playlist_id=playlist_id, track_id=track_id)
    db.session.add(playlist_track)
    db.session.commit()
    
    return jsonify({"message": "Track added to playlist"}), 201


@tracks_bp.route("/playlist/<int:playlist_id>/tracks/<int:track_id>", methods=["DELETE"])
def remove_track_from_playlist(playlist_id, track_id):
    """Remove a track from a playlist"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Verify user owns this playlist
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    
    # Find and delete the track from playlist
    playlist_track = PlaylistTrack.query.filter_by(
        playlist_id=playlist_id,
        track_id=track_id
    ).first()
    
    if not playlist_track:
        return jsonify({"error": "Track not in playlist"}), 404
    
    db.session.delete(playlist_track)
    db.session.commit()
    
    return jsonify({"message": "Track removed from playlist"}), 200


@tracks_bp.route("", methods=["POST"])
def create_track():
    """Create a new track (Admin only)"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Check if user is admin
    from models import User
    user = User.query.filter_by(id=user_id).first()
    if not user or user.role != 'ADMIN':
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.json
    title = data.get("title")
    artist_id = data.get("artist_id")
    spotify_id = data.get("spotify_id")
    duration_ms = data.get("duration_ms")
    
    if not title:
        return jsonify({"error": "Title required"}), 400
    
    track = Track(
        title=title,
        artist_id=artist_id,
        spotify_id=spotify_id,
        duration_ms=duration_ms
    )
    
    db.session.add(track)
    db.session.commit()
    
    return jsonify({
        "message": "Track created",
        "id": track.id,
        "title": track.title
    }), 201