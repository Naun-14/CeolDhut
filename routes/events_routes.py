from flask import Blueprint, request, jsonify
from models import db, Event, EventRegistration, User
import jwt
from datetime import datetime
import os

events_bp = Blueprint("events", __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'ceoldhut key')


def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None


@events_bp.route("", methods=["GET"])
def get_all_events():
    """Get all events"""
    
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
    """Get a specific event"""
    
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
def create_event():
    """Create a new event (Admin only)"""
    
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
    
    data = request.json
    title = data.get("title")
    location = data.get("location")
    event_date = data.get("event_date")
    description = data.get("description")
    
    if not title:
        return jsonify({"error": "Title required"}), 400
    
    # Parse event_date if provided
    parsed_date = None
    if event_date:
        try:
            parsed_date = datetime.fromisoformat(event_date)
        except:
            return jsonify({"error": "Invalid date format"}), 400
    
    event = Event(
        title=title,
        location=location,
        event_date=parsed_date,
        description=description,
        created_by=user_id
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        "message": "Event created",
        "id": event.id,
        "title": event.title
    }), 201


@events_bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    """Update an event (Admin only)"""
    
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
    
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.json
    
    if "title" in data:
        event.title = data.get("title")
    if "location" in data:
        event.location = data.get("location")
    if "description" in data:
        event.description = data.get("description")
    if "event_date" in data:
        try:
            event.event_date = datetime.fromisoformat(data.get("event_date"))
        except:
            return jsonify({"error": "Invalid date format"}), 400
    
    db.session.commit()
    
    return jsonify({
        "message": "Event updated",
        "id": event.id,
        "title": event.title
    }), 200


@events_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Delete an event (Admin only)"""
    
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
    
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({"message": "Event deleted"}), 200


@events_bp.route("/<int:event_id>/register", methods=["POST"])
def register_for_event(event_id):
    """Register a user for an event"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Check if event exists
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Check if already registered
    existing = EventRegistration.query.filter_by(
        user_id=user_id,
        event_id=event_id
    ).first()
    
    if existing:
        return jsonify({"error": "Already registered for this event"}), 400
    
    # Register user
    registration = EventRegistration(user_id=user_id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    
    return jsonify({"message": "Registered for event"}), 201


@events_bp.route("/<int:event_id>/register", methods=["DELETE"])
def unregister_from_event(event_id):
    """Unregister a user from an event"""
    
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    # Find registration
    registration = EventRegistration.query.filter_by(
        user_id=user_id,
        event_id=event_id
    ).first()
    
    if not registration:
        return jsonify({"error": "Not registered for this event"}), 404
    
    db.session.delete(registration)
    db.session.commit()
    
    return jsonify({"message": "Unregistered from event"}), 200


@events_bp.route("/<int:event_id>/registrations", methods=["GET"])
def get_event_registrations(event_id):
    """Get all users registered for an event (Admin only)"""
    
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
    
    # Check if event exists
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