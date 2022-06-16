"""Testing film crud"""

from pydantic import ValidationError
import pytest


from app import DATABASE
from app.crud import FILM
from app.models import Genre, Director, Film
from app.schemas import FilmBase


@pytest.mark.parametrize(
    "data, directors, genres, valid",
    [
        ({
            "title": "Ronny",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         True
        ),
        ({
            "title": "Ronny 2",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         True
        ),
        ({
            "title": "Ronny 3",
            "poster": "www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         False
        ),
        ({
            "title": "peaky Blinders",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         False
        ),
        ({
            "title": "Peaky124",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         False
        ),
        ({
            "title": "Peaky Blinders 2",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2025-09-12",
            "rating": 9.5,
            "user_id": 4
        },
         "1&2&4",
         "5&4",
         False
        )
    ]
)
def test_create_film(app_with_data, data, directors, genres, valid):
    """Check record creation with all relationships"""
    genres_id = genres.split('&')
    directors_id = directors.split('&')
    directors = [DATABASE.session.query(Director).get(i) for i in directors_id]
    genres = [DATABASE.session.query(Genre).get(i) for i in genres_id]
    try:
        film = FILM.create(database=DATABASE.session, obj_in=data,
                           directors=directors, genres=genres)
        assert valid
        assert isinstance(film, FilmBase)
        assert len(film.genres) == 2
        assert len(film.directors) == 3
    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "title, count",
    [("Mar", 2), ("Evening", 1), ("other", 1)])
def test_get_multy_by_title(app_with_data, title, count):
    """Checking the search for a partial match of the name"""
    films = FILM.get_multi_by_title(title=title, database=DATABASE.session).dict()['__root__']
    assert len(films) == count
    assert all(title.lower() in film['title'].lower() for film in films)


@pytest.mark.parametrize(
    "date_range, count",
    [("2001-2009", 2), ("2015-2019", 3)])
def test_date_filter(app_with_data, date_range, count):
    """Check filter by date"""
    query = DATABASE.session.query(Film).distinct()
    films = FILM.date_filter(query, date_range).all()
    assert len(films) == count


@pytest.mark.parametrize(
    "directors, count",
    [("John_Johnson", 2), ("Jack_Jackson", 3), ("John_Johnson&Jack_Jackson", 4)])
def test_director_filter(app_with_data, directors, count):
    """Checking the filter by directors"""
    query = DATABASE.session.query(Film).distinct()
    films = FILM.director_filter(query, directors).all()
    assert len(films) == count


@pytest.mark.parametrize(
    "genres, count",
    [('Action', 3), ('Drama', 2), ('Fantasy', 2),
     ('Action&Drama', 4), ('Fantasy&Drama', 3)])
def test_genre_filter(app_with_data, genres, count):
    """Check filter by genres"""
    query = DATABASE.session.query(Film).distinct()
    films = FILM.genre_filter(query, genres).all()
    assert len(films) == count


@pytest.mark.parametrize(
    "data, count",
    [([None, None, 'Action&Drama'], 4), ([None, "John_Johnson", 'Action'], 2),
     (["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 2),
     (["2015-2019", "Jack_Jackson", "Drama"], 1)])
def test_multy_filter(app_with_data, data, count):
    """Checking the multifilter"""
    films = FILM.query_film_multy_filter(database=DATABASE.session, values=data).dict()['__root__']
    assert len(films) == count


def test_sort_rating_asc(app_with_data):
    """Checking the sorting of movies by rating in ascending order"""
    alchemy = FILM.rating_asc(query=DATABASE.session.query(Film)).all()
    db = DATABASE.session.execute("SELECT * from film ORDER BY rating").all()
    assert [film.film_id for film in alchemy] == [query[0] for query in db]


def test_sort_rating_desc(app_with_data):
    """Checking the sorting of movies by rating in descending order"""
    alchemy = FILM.rating_desc(query=DATABASE.session.query(Film)).all()
    db = DATABASE.session.execute("SELECT * from film ORDER BY rating DESC").all()
    assert [film.film_id for film in alchemy] == [query[0] for query in db]


def test_sort_date_asc(app_with_data):
    """Checking the sorting of movies by release date in ascending order"""
    alchemy = FILM.date_asc(query=DATABASE.session.query(Film)).all()
    db = DATABASE.session.execute("SELECT * from film ORDER BY release_date").all()
    assert [film.film_id for film in alchemy] == [query[0] for query in db]


def test_sort_date_desc(app_with_data):
    """Checking the sorting of movies by release date in descending order"""
    alchemy = FILM.date_desc(query=DATABASE.session.query(Film)).all()
    db = DATABASE.session.execute("SELECT * from film ORDER BY release_date DESC").all()
    assert [film.film_id for film in alchemy] == [query[0] for query in db]


@pytest.mark.parametrize(
    "data, postgres_query",
    [([None, "asc"], "SELECT * from film ORDER BY rating"),
     (["desc", None], "SELECT * from film ORDER BY release_date DESC"),
     (["asc", "desc"], "SELECT * from film ORDER BY release_date, rating DESC"),
     (["asc", "asc"], "SELECT * from film ORDER BY release_date, rating")])
def test_multy_sort(app_with_data, data, postgres_query):
    """Multisort check"""
    alchemy = FILM.query_film_multy_sort(database=DATABASE.session, order=data).dict()["__root__"]
    db = DATABASE.session.execute(postgres_query).all()
    assert [alchemy[i]['title'] == db[i][1] for i in range(len(alchemy))]
