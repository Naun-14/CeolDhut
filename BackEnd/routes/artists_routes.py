from flask import Blueprint, jsonify, request

from auth_utils import require_admin
from models import Artist, db

artists_bp = Blueprint("artists", __name__)


@artists_bp.route("", methods=["GET"])
def get_all_artists():
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
@require_admin
def create_artist():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    country = (data.get("country") or "").strip() or None
    spotify_id = (data.get("spotify_id") or "").strip() or None

    if not name:
        return jsonify({"error": "Artist name required"}), 400

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
@require_admin
def verify_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404

    artist.verified = True
    from flask import g
    artist.verified_by = g.current_user.id
    db.session.commit()

    return jsonify({
        "message": "Artist verified",
        "id": artist.id,
        "name": artist.name,
        "verified": True
    }), 200


@artists_bp.route("/<int:artist_id>", methods=["PUT"])
@require_admin
def update_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Artist name required"}), 400
        duplicate = Artist.query.filter(Artist.name == name, Artist.id != artist_id).first()
        if duplicate:
            return jsonify({"error": "Artist already exists"}), 400
        artist.name = name
    if "country" in data:
        artist.country = (data.get("country") or "").strip() or None
    if "spotify_id" in data:
        artist.spotify_id = (data.get("spotify_id") or "").strip() or None

    db.session.commit()

    return jsonify({
        "message": "Artist updated",
        "id": artist.id,
        "name": artist.name
    }), 200


@artists_bp.route("/<int:artist_id>", methods=["DELETE"])
@require_admin
def delete_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        return jsonify({"error": "Artist not found"}), 404

    db.session.delete(artist)
    db.session.commit()

    return jsonify({"message": "Artist deleted"}), 200
