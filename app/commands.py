"""Module for cli commands"""

from faker import Faker
from flask import Blueprint
from .crud import DIRECTOR, FILM, GENRE, ROLE, USER
from .models import Director, Genre
from .models.db_init import DATABASE

cmd = Blueprint('cmd', __name__, cli_group=None)  # pylint: disable=C0103
FAKER = Faker()


def seed_director():
    """Method for seeding director table"""
    for _ in range(100):
        director_values = {'name': FAKER.first_name(), 'surname': FAKER.last_name()}
        DIRECTOR.create(database=DATABASE.session(), obj_in=director_values)


def seed_role():
    """Method for seeding role table"""
    ROLE.create(database=DATABASE.session(), obj_in={'name': 'user'})
    ROLE.create(database=DATABASE.session(), obj_in={'name': 'admin'})


def seed_user():
    """Method for seeding user table"""
    for _ in range(100):
        user_values = {'role_id': FAKER.random_int(1, 2), 'name': FAKER.first_name(),
                       'email': FAKER.email(), 'password': FAKER.password()}
        USER.create(database=DATABASE.session(), obj_in=user_values)


def seed_genre():
    """Method for seeding genre table"""
    genres = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror',
              'Mystery', 'Romance', 'Thriller', 'Western']
    for item in genres:
        genre_value = {'genre_name': item}
        GENRE.create(database=DATABASE.session(), obj_in=genre_value)


def seed_film():
    """Method for seeding film table"""
    for _ in range(100):
        directors_id = set(FAKER.pyint(1, 100) for _ in range(3))
        genres_id = set(FAKER.pyint(1, 9) for _ in range(3))
        film_values = {
            'user_id': FAKER.pyint(1, 100), 'title': ' '.join(FAKER.words(3)).capitalize(),
            'poster': FAKER.url(), 'description': FAKER.text(), 'release_date': FAKER.date(),
            'rating': round(FAKER.pyfloat(min_value=0, max_value=10), 1)
        }
        FILM.create(
            database=DATABASE.session(), obj_in=film_values,
            directors=[DATABASE.session.query(Director).get(dir_id) for dir_id in directors_id],
            genres=[DATABASE.session.query(Genre).get(genre_id) for genre_id in genres_id]
        )


@cmd.cli.command('seed_all')
def seed_all():
    """Method for seeding all tables"""
    seed_role()
    seed_user()
    seed_director()
    seed_genre()
    seed_film()
