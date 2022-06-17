"""Module with film_genre association table"""

from .db_init import db

film_genre = db.Table(
    "film_genre",
    db.Column("film_id", db.ForeignKey("film.film_id"), primary_key=True),
    db.Column("genre_id", db.ForeignKey("genre.genre_id"), primary_key=True)
)
