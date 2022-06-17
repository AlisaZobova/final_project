"""Fixtures for testing"""

from datetime import datetime

from faker import Faker
import pytest

from app import create_app, User
from app.models import Role, Director, Genre, Film
from app.models.db_init import db
from tests.config import Config


@pytest.fixture(scope="function", autouse=True)
def flask_app():
    """Fixture with test client"""
    app = create_app(conf=Config)
    app.testing = True

    client = app.test_client()

    context = app.test_request_context()
    context.push()

    yield client

    context.pop()


@pytest.fixture(scope="function", autouse=True)
def app_with_db(flask_app):
    """Fixture with empty test database"""
    db.create_all()

    yield flask_app

    db.drop_all()


def seed():
    """Function for seeding test database"""
    faker = Faker()

    for _ in range(10):
        director_values = {'name': faker.first_name(), 'surname': faker.last_name()}
        db.session.add(Director(**director_values))

    db.session.add(Director(**{'name': "John", 'surname': "Johnson"}))
    db.session.add(Director(**{'name': "Jack", 'surname': "Jackson"}))

    db.session.add(Role(**{'name': 'user'}))
    db.session.add(Role(**{'name': 'admin'}))

    for _ in range(10):
        user_values = {'role_id': faker.random_int(1, 2), 'name': faker.first_name(),
                       'email': faker.email(), 'password': faker.password()}
        db.session.add(User(**user_values))

    db.session.add(User(**{
        'role_id': 2,
        'name': faker.first_name(),
        "email": "john@gmail.com",
        "password": "Johny5863"
    }))

    db.session.add(User(**{
        'role_id': 1,
        'name': faker.first_name(),
        "email": "jacky@gmail.com",
        "password": "Jacky"
    }))

    genres = ['Action', 'Drama', 'Fantasy', 'Horror',
              'Mystery', 'Romance', 'Thriller', 'Western']
    for item in genres:
        genre_value = {'genre_name': item}
        db.session.add(Genre(**genre_value))

    titles = ["Mary Johnson", "On the other side",
              "Evening in Manhattan", "Mark per million", "Winner"]
    for title in titles:
        if titles.index(title) % 2 == 0:
            film_values = {
                'user_id': 6, 'title': title,
                'poster': faker.url(), 'description': faker.text(),
                'release_date': faker.date_between_dates(date_start=datetime(2015, 1, 1),
                                                         date_end=datetime(2019, 12, 31)),
                'rating': round(faker.pyfloat(min_value=0, max_value=10), 1)
            }
        else:
            film_values = {
                'user_id': 6, 'title': title,
                'poster': faker.url(), 'description': faker.text(),
                'release_date': faker.date_between_dates(date_start=datetime(2001, 1, 1),
                                                         date_end=datetime(2009, 12, 31)),
                'rating': round(faker.pyfloat(min_value=0, max_value=10), 1)
            }
        db.session.add(Film(**film_values))


@pytest.fixture(scope="function", autouse=True)
def app_with_data(app_with_db):
    """Fixture with test database with data"""

    seed()

    director1 = db.session.query(Director).get(11)
    director2 = db.session.query(Director).get(12)

    genre1 = db.session.query(Genre).get(1)
    genre2 = db.session.query(Genre).get(2)
    genre3 = db.session.query(Genre).get(3)

    film = db.session.query(Film).get(1)
    film.directors.append(director1)
    film.genres.append(genre1)
    film.genres.append(genre3)

    film = db.session.query(Film).get(2)
    film.directors.append(director1)
    film.directors.append(director2)
    film.genres.append(genre1)
    film.genres.append(genre2)

    film = db.session.query(Film).get(3)
    film.directors.append(director2)
    film.genres.append(genre2)
    film.genres.append(genre3)

    film = db.session.query(Film).get(4)
    film.directors.append(director2)
    film.genres.append(genre1)

    db.session.commit()

    yield app_with_db

    db.session.execute("TRUNCATE role CASCADE;")
    db.session.execute('TRUNCATE "user" CASCADE;')
    db.session.execute("TRUNCATE director CASCADE;")
    db.session.execute("TRUNCATE genre CASCADE;")
    db.session.execute("TRUNCATE film CASCADE;")

    db.session.commit()
