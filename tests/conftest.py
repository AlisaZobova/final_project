"""Fixtures for testing"""

from datetime import datetime

from faker import Faker
import pytest

from app import create_app, User
from app.models import Role, Director, Genre, Film
from app.models.db_init import DATABASE
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
    DATABASE.create_all()

    yield flask_app

    DATABASE.drop_all()


@pytest.fixture(scope="function", autouse=True)
def app_with_data(app_with_db):
    """Fixture with test database with data"""
    faker = Faker()

    for _ in range(10):
        director_values = {'name': faker.first_name(), 'surname': faker.last_name()}
        DATABASE.session.add(Director(**director_values))

    director_values = {'name': "John", 'surname': "Johnson"}
    DATABASE.session.add(Director(**director_values))

    director_values = {'name': "Jack", 'surname': "Jackson"}
    DATABASE.session.add(Director(**director_values))

    user_role = Role(**{'name': 'user'})
    admin_role = Role(**{'name': 'admin'})
    DATABASE.session.add(user_role)
    DATABASE.session.add(admin_role)

    for _ in range(10):
        user_values = {'role_id': faker.random_int(1, 2), 'name': faker.first_name(),
                       'email': faker.email(), 'password': faker.password()}
        DATABASE.session.add(User(**user_values))

    DATABASE.session.add(User(**{
        'role_id': 2,
        'name': faker.first_name(),
        "email": "john@gmail.com",
        "password": "Johny5863"
        }))

    DATABASE.session.add(User(**{
        'role_id': 1,
        'name': faker.first_name(),
        "email": "jacky@gmail.com",
        "password": "Jacky"
        }))

    genres = ['Action', 'Drama', 'Fantasy', 'Horror',
              'Mystery', 'Romance', 'Thriller', 'Western']
    for item in genres:
        genre_value = {'genre_name': item}
        DATABASE.session.add(Genre(**genre_value))

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
        DATABASE.session.add(Film(**film_values))

    director1 = DATABASE.session.query(Director).get(11)
    director2 = DATABASE.session.query(Director).get(12)

    genre1 = DATABASE.session.query(Genre).get(1)
    genre2 = DATABASE.session.query(Genre).get(2)
    genre3 = DATABASE.session.query(Genre).get(3)

    film = DATABASE.session.query(Film).get(1)
    film.directors.append(director1)
    film.genres.append(genre1)
    film.genres.append(genre3)

    film = DATABASE.session.query(Film).get(2)
    film.directors.append(director1)
    film.directors.append(director2)
    film.genres.append(genre1)
    film.genres.append(genre2)

    film = DATABASE.session.query(Film).get(3)
    film.directors.append(director2)
    film.genres.append(genre2)
    film.genres.append(genre3)

    film = DATABASE.session.query(Film).get(4)
    film.directors.append(director2)
    film.genres.append(genre1)

    DATABASE.session.commit()

    yield app_with_db

    DATABASE.session.execute("TRUNCATE role CASCADE;")
    DATABASE.session.execute('TRUNCATE "user" CASCADE;')
    DATABASE.session.execute("TRUNCATE director CASCADE;")
    DATABASE.session.execute("TRUNCATE genre CASCADE;")
    DATABASE.session.execute("TRUNCATE film CASCADE;")

    DATABASE.session.commit()
