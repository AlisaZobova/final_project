from . import db


class Genre(db.Model):
    """Class to store genres"""
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.VARCHAR(50), unique=True)
