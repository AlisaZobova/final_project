"""Module with film orm model"""

from .db_init import db
from .film_director import film_director
from .film_genre import film_genre


class Film(db.Model):
    """Class to store films and information about them"""
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    poster = db.Column(db.VARCHAR(100), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    directors = db.relationship("Director", secondary=film_director, backref="films")
    genres = db.relationship("Genre", secondary=film_genre, backref="films")
