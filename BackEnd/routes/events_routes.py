from datetime import datetime

from flask import Blueprint, g, jsonify, request

from auth_utils import require_admin, require_auth
from models import Event, EventRegistration, db

events_bp = Blueprint("events", __name__)


@events_bp.route("", methods=["GET"])
def get_all_events():
    events = Event.query.all()

    return jsonify({
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "location": e.location,
                "event_date": e.event_date.isoformat() if e.event_date else None,
                "description": e.description,
                "created_at": e.created_at.isoformat()
            }
            for e in events
        ]
    }), 200


@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.filter_by(id=event_id).first()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({
        "id": event.id,
        "title": event.title,
        "location": event.location,
        "event_date": event.event_date.isoformat() if event.event_date else None,
        "description": event.description,
        "created_at": event.created_at.isoformat()
    }), 200


@events_bp.route("", methods=["POST"])
@require_admin
def create_event():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    location = (data.get("location") or "").strip() or None
    event_date = data.get("event_date")
    description = (data.get("description") or "").strip() or None

    if not title:
        return jsonify({"error": "Title required"}), 400

    parsed_date = None
    if event_date:
        try:
            parsed_date = datetime.fromisoformat(event_date)
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    event = Event(
        title=title,
        location=location,
        event_date=parsed_date,
        description=description,
        created_by=g.current_user.id
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "message": "Event created",
        "id": event.id,
        "title": event.title
    }), 201


@events_bp.route("/<int:event_id>", methods=["PUT"])
@require_admin
def update_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Title required"}), 400
        event.title = title
    if "location" in data:
        event.location = (data.get("location") or "").strip() or None
    if "description" in data:
        event.description = (data.get("description") or "").strip() or None
    if "event_date" in data:
        if not data.get("event_date"):
            event.event_date = None
        else:
            try:
                event.event_date = datetime.fromisoformat(data.get("event_date"))
            except ValueError:
                return jsonify({"error": "Invalid date format"}), 400

    db.session.commit()

    return jsonify({
        "message": "Event updated",
        "id": event.id,
        "title": event.title
    }), 200


@events_bp.route("/<int:event_id>", methods=["DELETE"])
@require_admin
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted"}), 200


@events_bp.route("/<int:event_id>/register", methods=["POST"])
@require_auth
def register_for_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    existing = EventRegistration.query.filter_by(
        user_id=g.current_user.id,
        event_id=event_id
    ).first()

    if existing:
        return jsonify({"error": "Already registered for this event"}), 400

    registration = EventRegistration(user_id=g.current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()

    return jsonify({"message": "Registered for event"}), 201


@events_bp.route("/<int:event_id>/register", methods=["DELETE"])
@require_auth
def unregister_from_event(event_id):
    registration = EventRegistration.query.filter_by(
        user_id=g.current_user.id,
        event_id=event_id
    ).first()

    if not registration:
        return jsonify({"error": "Not registered for this event"}), 404

    db.session.delete(registration)
    db.session.commit()

    return jsonify({"message": "Unregistered from event"}), 200


@events_bp.route("/<int:event_id>/registrations", methods=["GET"])
@require_admin
def get_event_registrations(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    registrations = EventRegistration.query.filter_by(event_id=event_id).all()

    users = [
        {
            "user_id": reg.user_id,
            "registered_at": reg.registered_at.isoformat()
        }
        for reg in registrations
    ]
    
    return jsonify({"registrations": users}), 200
