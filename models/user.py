"""Module with USER orm model"""

from .db_init import DATABASE


class User(DATABASE.Model):
    """Class to store users and information about them"""
    __tablename__ = 'user'
    user_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    role_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('role.role_id'), nullable=False)
    name = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    email = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    password = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    films = DATABASE.relationship('Film', backref=DATABASE.backref('user'))

    def __str__(self):
        return f'User {self.user_id}: {self.name} - {self.email}'
