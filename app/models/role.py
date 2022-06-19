"""Module with role orm model"""

from .db_init import db


class Role(db.Model):
    """Class to store user roles"""
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50), unique=True)
    users = db.relationship('User', backref=db.backref('role'))
