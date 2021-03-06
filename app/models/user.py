"""Module with user orm model"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .db_init import db


class User(UserMixin, db.Model):
    """Class to store users and information about them"""
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(255), nullable=False)
    films = db.relationship('Film', backref='user', cascade='all, delete')

    def __init__(self, role_id, name, email, password):
        self.role_id = role_id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def get_id(self):
        """Override UserMixin method"""
        return self.user_id

    def __str__(self):
        return f'User {self.user_id}: {self.name} - {self.email}'
