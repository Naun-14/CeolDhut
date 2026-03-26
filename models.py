from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='USER', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Playlist {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'
    
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Artist {self.name}>'


class Track(db.Model):
    __tablename__ = 'tracks'
    
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255), unique=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    title = db.Column(db.String(255), nullable=False)
    duration_ms = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ADD THIS:
    artist = db.relationship('Artist', backref='tracks')
    
    def __repr__(self):
        return f'<Track {self.title}>'


class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    event_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.title}>'


class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)