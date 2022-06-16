"""Testing film domain functions"""

from typing import Dict

import pytest

from app import DATABASE
from app.crud import FILM
from app.domain import create_film, set_unknown_director, set_unknown_director_multy
from app.models import Film
from app.schemas import FilmBase


@pytest.mark.parametrize(
    "data, directors_id, genres_id",
    [
        ({
             "title": "Jack",
             "poster": "https://www.posters.net/Peaky-Blinders-poster",
             "description": "A gangster family epic set in 1900s England.",
             "release_date": "2013-09-12",
             "rating": 9.5,
             "user_id": 4
         },
         "10",
         "4"
        ),
        ({
             "title": "History of success",
             "poster": "https://www.posters.net/Peaky-Blinders-poster",
             "description": "A gangster family epic set in 1900s England.",
             "release_date": "2013-09-12",
             "rating": 7.6,
             "user_id": 4
         },
        "10",
        "4")
    ]
)
def test_create_film(app_with_data, data, directors_id, genres_id):
    """
    Checking the correctness of the creation of the film
    and the type of the value returned by the function
    """
    film = create_film(FILM, values=data, directors_id=directors_id, genres_id=genres_id)
    assert isinstance(film, Dict)


def test_set_unknown_director(app_with_data):
    """Checking if the directors field is UNKNOWN if the movie has no directors"""
    film = FilmBase.from_orm(DATABASE.session.query(Film).get(5)).dict()
    unknown = set_unknown_director(film)
    assert unknown['directors'] == 'UNKNOWN'


def test_set_unknown_multy():
    """Checking if the directors field is UNKNOWN if the movie has no directors"""
    films = FILM.get_multi(database=DATABASE.session).dict()
    assert set_unknown_director_multy(films)['__root__'][4]['directors'] == 'UNKNOWN'
