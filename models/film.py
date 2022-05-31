from . import db
from . import film_director
from . import film_genre


class Film(db.Model):
    """Class to store films and information about them"""
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(50), nullable=False)
    poster = db.Column(db.VARCHAR(50), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    directors = db.relationship("Director", secondary=film_director, backref=db.backref("films"))
    genres = db.relationship("Genre", secondary=film_genre, backref=db.backref("films"))
