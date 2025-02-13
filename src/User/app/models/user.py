# app/models/user.py

from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False) # "user" or "admin"
    is_active = db.Column(db.Boolean, default=True)  
    is_blocked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'



