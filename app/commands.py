"""Module for cli commands"""

from faker import Faker
from flask import Blueprint
from .crud import director, film, genre, user
from .models import Role
from .models.db_init import db

cmd = Blueprint('cmd', __name__, cli_group=None)
fake = Faker()


def seed_director():
    """Method for seeding director table"""
    for _ in range(100):
        director_values = {'name': fake.first_name(), 'surname': fake.last_name()}
        director.create(obj_in=director_values)


def seed_role():
    """Method for seeding role table"""
    user_role = Role(**{'name': 'user'})
    admin_role = Role(**{'name': 'admin'})
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.commit()


def seed_user():
    """Method for seeding user table"""
    for _ in range(100):
        user_values = {'role_id': fake.random_int(1, 2), 'name': fake.first_name(),
                       'email': fake.email(), 'password': fake.password()}
        user.create(obj_in=user_values)


def seed_genre():
    """Method for seeding genre table"""
    genres = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror',
              'Mystery', 'Romance', 'Thriller', 'Western']
    for item in genres:
        genre_value = {'genre_name': item}
        genre.create(obj_in=genre_value)


def seed_film():
    """Method for seeding film table"""
    for _ in range(100):
        directors_id = set(fake.pyint(1, 100) for _ in range(3))
        genres_id = set(fake.pyint(1, 9) for _ in range(3))
        film_values = {
            'user_id': fake.pyint(1, 100), 'title': ' '.join(fake.words(3)).capitalize(),
            'poster': fake.url(), 'description': fake.text(), 'release_date': fake.date(),
            'rating': round(fake.pyfloat(min_value=0, max_value=10), 1)
        }
        film.create(
            obj_in=film_values,
            directors=list(directors_id),
            genres=list(genres_id)
        )


@cmd.cli.command('seed_all')
def seed_all():
    """Method for seeding all tables"""
    seed_role()
    seed_user()
    seed_director()
    seed_genre()
    seed_film()
