"""Module with FILM_DIRECTOR association table"""

from .db_init import DATABASE

FILM_DIRECTOR = DATABASE.Table(
    "film_director",
    DATABASE.Column("film_id", DATABASE.ForeignKey("film.film_id"), primary_key=True),
    DATABASE.Column("director_id", DATABASE.ForeignKey("director.director_id"), primary_key=True)
)
