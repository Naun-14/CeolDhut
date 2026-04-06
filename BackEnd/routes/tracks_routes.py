from flask import Blueprint, g, jsonify, request

from auth_utils import require_auth
from models import db, Track, Playlist, PlaylistTrack, Artist

tracks_bp = Blueprint("tracks", __name__)


@tracks_bp.route("/playlist/<int:playlist_id>/tracks", methods=["GET"])
@require_auth
def get_playlist_tracks(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=g.current_user.id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

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
@require_auth
def add_track_to_playlist(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=g.current_user.id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    data = request.get_json(silent=True) or {}
    track_id = data.get("track_id")

    if not track_id:
        return jsonify({"error": "Track ID required"}), 400

    track = Track.query.filter_by(id=track_id).first()
    if not track:
        return jsonify({"error": "Track not found"}), 404

    existing = PlaylistTrack.query.filter_by(
        playlist_id=playlist_id,
        track_id=track_id
    ).first()

    if existing:
        return jsonify({"error": "Track already in playlist"}), 400

    playlist_track = PlaylistTrack(playlist_id=playlist_id, track_id=track_id)
    db.session.add(playlist_track)
    db.session.commit()

    return jsonify({"message": "Track added to playlist"}), 201


@tracks_bp.route("/playlist/<int:playlist_id>/tracks/<int:track_id>", methods=["DELETE"])
@require_auth
def remove_track_from_playlist(playlist_id, track_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=g.current_user.id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

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
@require_auth
def create_track():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    artist_id = data.get("artist_id")
    spotify_id = data.get("spotify_id")
    duration_ms = data.get("duration_ms")

    if not title:
        return jsonify({"error": "Title required"}), 400
    if artist_id and not Artist.query.filter_by(id=artist_id).first():
        return jsonify({"error": "Artist not found"}), 404

    existing_track = None
    if spotify_id:
        existing_track = Track.query.filter_by(spotify_id=spotify_id).first()
    elif title and artist_id:
        existing_track = Track.query.filter_by(title=title, artist_id=artist_id).first()

    if existing_track:
        return jsonify({
            "message": "Track already exists",
            "id": existing_track.id,
            "title": existing_track.title
        }), 200
    
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
