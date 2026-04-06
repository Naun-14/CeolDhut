from flask import Blueprint, g, jsonify, request

from auth_utils import require_auth
from models import db, Playlist

playlist_bp = Blueprint("playlists", __name__)


@playlist_bp.route("", methods=["GET"])
@require_auth
def get_playlists():
    playlists = Playlist.query.filter_by(user_id=g.current_user.id).all()

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
@require_auth
def create_playlist():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Playlist name required"}), 400
    if Playlist.query.filter_by(user_id=g.current_user.id, name=name).first():
        return jsonify({"error": "Playlist already exists"}), 400

    new_playlist = Playlist(
        user_id=g.current_user.id,
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
@require_auth
def update_playlist(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=g.current_user.id).first()

    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Playlist name required"}), 400
    if Playlist.query.filter(
        Playlist.user_id == g.current_user.id,
        Playlist.name == name,
        Playlist.id != playlist_id,
    ).first():
        return jsonify({"error": "Playlist already exists"}), 400

    playlist.name = name
    db.session.commit()

    return jsonify({
        "message": "Playlist updated",
        "id": playlist.id,
        "name": playlist.name
    }), 200


@playlist_bp.route("/<int:playlist_id>", methods=["DELETE"])
@require_auth
def delete_playlist(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=g.current_user.id).first()

    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    db.session.delete(playlist)
    db.session.commit()

    return jsonify({"message": "Playlist deleted"}), 200
