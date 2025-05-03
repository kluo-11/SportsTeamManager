# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Team(db.Model):
    __tablename__ = 'Teams'
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sport = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    events = db.relationship('Event', backref='team', lazy=True)

class Player(db.Model):
    __tablename__ = 'Players'
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    attendance_records = db.relationship('Attendance', backref='player', lazy=True)

class Event(db.Model):
    __tablename__ = 'Events'
    event_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    event_type = db.Column(db.String(255))
    event_date = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    attendance = db.relationship('Attendance', backref='event', lazy=True)
    match = db.relationship('Match', backref='event', uselist=False)

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.event_id'))
    player_id = db.Column(db.Integer, db.ForeignKey('Players.player_id'))
    status = db.Column(db.String(255))

class Match(db.Model):
    __tablename__ = 'Matches'
    match_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.event_id'), unique=True)
    opponent_team = db.Column(db.String(255), nullable=False)
    team_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)
    result = db.Column(db.String(255))
