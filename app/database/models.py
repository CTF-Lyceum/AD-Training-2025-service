from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator_username = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    visibility = db.Column(db.String, nullable=False)
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    creator = db.relationship('User', backref=db.backref('notes', lazy=True))
