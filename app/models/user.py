"""Module with USER orm model"""
from flask_login import UserMixin
from .db_init import DATABASE


class User(UserMixin, DATABASE.Model):
    """Class to store users and information about them"""
    __tablename__ = 'user'
    user_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    role_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('role.role_id'), nullable=False)
    name = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    email = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False, unique=True)
    password = DATABASE.Column(DATABASE.VARCHAR(255), nullable=False)
    films = DATABASE.relationship('Film', backref='user', cascade='all, delete')

    def get_id(self):
        """Override UserMixin method"""
        return self.user_id

    def __str__(self):
        return f'User {self.user_id}: {self.name} - {self.email}'
