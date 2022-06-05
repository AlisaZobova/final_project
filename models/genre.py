"""Module with GENRE orm model"""

from .db_init import DATABASE


class Genre(DATABASE.Model):
    """Class to store genres"""
    __tablename__ = 'genre'
    genre_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    genre_name = DATABASE.Column(DATABASE.VARCHAR(50), unique=True)
