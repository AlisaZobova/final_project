"""Module with FILM_GENRE association table"""

from .db_init import DATABASE

FILM_GENRE = DATABASE.Table(
    "film_genre",
    DATABASE.Column("film_id", DATABASE.ForeignKey("film.film_id"), primary_key=True),
    DATABASE.Column("genre_id", DATABASE.ForeignKey("genre.genre_id"), primary_key=True)
)
