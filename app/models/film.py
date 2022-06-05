"""Module with FILM orm model"""

from .db_init import DATABASE
from .film_director import FILM_DIRECTOR
from .film_genre import FILM_GENRE


class Film(DATABASE.Model):
    """Class to store films and information about them"""
    __tablename__ = 'film'
    film_id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.user_id'), nullable=False)
    title = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    poster = DATABASE.Column(DATABASE.VARCHAR(50), nullable=False)
    description = DATABASE.Column(DATABASE.Text)
    release_date = DATABASE.Column(DATABASE.Date, nullable=False)
    rating = DATABASE.Column(DATABASE.Float, nullable=False)
    directors = DATABASE.relationship("Director", secondary=FILM_DIRECTOR, backref="films", cascade='all, delete')
    genres = DATABASE.relationship("Genre", secondary=FILM_GENRE, backref="films", cascade='all, delete')
