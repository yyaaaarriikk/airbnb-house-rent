from app import db 
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    country = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    country = db.Column(db.String, nullable = False)
    address = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    residents = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    image = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='не заброньовано')

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    booking_name = db.Column(db.String, nullable=False)
    arrival_date = db.Column(db.Integer, nullable = False)
    departure_date = db.Column(db.Integer, nullable = False)
    arrival_residents = db.Column(db.Integer, nullable = False)
    create_at = db.Column(db.DateTime, default = datetime.utcnow)
    house = db.relationship('House', backref='booking', lazy=True)
    user = db.relationship('User', backref='booking', lazy=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


# class Survey(db.Model):
#     __tablename__ = 'survey'
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String, nullable=False)
#     options = relationship('Option', backref='survey', lazy=True)

# class Option(db.Model):
#     __tablename__ = 'option'
#     id = db.Column(db.Integer, primary_key=True)
#     option_text = db.Column(db.String, nullable=False)
#     votes = db.Column(db.Integer, default=0)
#     survey_id = db.Column(db.ForeignKey('survey.id'), nullable=False)
