"""Module with DIRECTOR orm model"""

from .db_init import DATABASE


class Director(DATABASE.Model):
    """Class to store directors and information about them"""
    __tablename__ = 'director'
    director_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    surname = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
