from . import db

film_director = db.Table(
    "film_director",
    db.Column("film_id", db.ForeignKey("film.film_id"), primary_key=True),
    db.Column("director_id", db.ForeignKey("director.director_id"), primary_key=True),
)
