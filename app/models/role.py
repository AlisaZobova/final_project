"""Module with ROLE orm model"""

from .db_init import DATABASE


class Role(DATABASE.Model):
    """Class to store USER roles"""
    __tablename__ = 'role'
    role_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.VARCHAR(50), unique=True)
    users = DATABASE.relationship('User', backref=DATABASE.backref('role'))
