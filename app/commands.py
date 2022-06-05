from faker import Faker
from flask import Blueprint
from .crud import DIRECTOR, FILM, GENRE, ROLE, USER
from .models import Director, Genre
from .models.db_init import DATABASE

cmd = Blueprint('cmd', __name__, cli_group=None)
faker = Faker()


def seed_director():
    for _ in range(100):
        director_values = {'name': faker.first_name(), 'surname': faker.last_name()}
        DIRECTOR.create(database=DATABASE.session(), obj_in=director_values)


def seed_role():
    ROLE.create(database=DATABASE.session(), obj_in={'name': 'USER'})
    ROLE.create(database=DATABASE.session(), obj_in={'name': 'admin'})


def seed_user():
    for _ in range(100):
        user_values = {'role_id': faker.random_int(1, 2), 'name': faker.first_name(),
                       'email': faker.email(), 'password': faker.password()}
        USER.create(database=DATABASE.session(), obj_in=user_values)


def seed_genre():
    genres = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror',
              'Mystery', 'Romance', 'Thriller', 'Western']
    for item in genres:
        genre_value = {'genre_name': item}
        GENRE.create(database=DATABASE.session(), obj_in=genre_value)


def seed_film():
    for _ in range(100):
        directors_id = set(faker.pyint(1, 100) for _ in range(3))
        genres_id = set(faker.pyint(1, 9) for _ in range(3))
        film_values = {'user_id': faker.pyint(1, 100), 'title': ' '.join(faker.words(3)).capitalize(),
                       'poster': faker.url(), 'description': faker.text(), 'release_date': faker.date(),
                       'rating': round(faker.pyfloat(min_value=0, max_value=10), 1)}
        FILM.create(database=DATABASE.session(), obj_in=film_values,
                    directors=[DATABASE.session.query(Director).get(dir_id) for dir_id in directors_id],
                    genres=[DATABASE.session.query(Genre).get(genre_id) for genre_id in genres_id])


@cmd.cli.command('seed_all')
def seed_all():
    seed_role()
    seed_user()
    seed_director()
    seed_genre()
    seed_film()
