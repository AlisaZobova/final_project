"""Testing film route_domain functions"""
from datetime import date
from typing import Dict, List
from unittest import mock
from flask import url_for
from pydantic import BaseModel

from app.schemas import FilmBase
from app.schemas.film import FilmList
from tests.end_to_end.endpoints.test_subfunctions import check_count


class FilmMock(BaseModel):
    """Mock film schema"""
    user_id: int
    title: str
    poster: str
    description: str
    release_date: date
    rating: float
    directors: List[int]
    genres: List[int]


def fake_film():
    """Function for mocking film crud"""
    class FakeFilmCRUD:
        """Mock film crud"""
        def get(self):
            """Mock get method"""
            return FilmBase.parse_obj({
                "title": "Jacky",
                "poster": "https://www.posters.net/Peaky-Blinders-poster",
                "description": "A gangster family epic set in 1900s England.",
                "release_date": "2013-09-12",
                "rating": 9.5,
                "user_id": 4,
                "directors": [],
                "genres": []
            })

        def create(self, obj_in, directors, genres):
            """Mock create method"""
            return FilmMock.parse_obj({
                "title": obj_in['title'],
                "poster": obj_in['poster'],
                "description": obj_in['description'],
                "release_date": obj_in['release_date'],
                "rating": obj_in['rating'],
                "user_id": obj_in['user_id'],
                "directors": directors,
                "genres": genres
            })

        def get_multi(self):
            """Mock get multi method"""
            films = FilmList.from_orm([self.get() for _ in range(10)])
            return films

    return FakeFilmCRUD()


def fake_user():
    """Function for mocking auth"""
    class FakeAuth:
        """Mock flask_login.utils"""
        def get_user(self):
            """Mock flask_login.utils._get_user"""
            current_user = mock.MagicMock()
            current_user.return_value = mock.Mock(is_authenticated=True, user_id=5)
            return current_user

    return FakeAuth()


@mock.patch("flask_login.utils._get_user", new=fake_user().get_user())
@mock.patch("app.crud.film.create", new=fake_film().create)
def test_create_film(flask_app):
    """
    Checks setting current user id and the correctness of the transfer of the
    list of IDs of genres and directors from the domain to the repository
    """
    response = flask_app.post(url_for("api.film_create"), json={
        "title": "Jacky",
        "poster": "https://www.posters.net/Peaky-Blinders-poster",
        "description": "A gangster family epic set in 1900s England.",
        "release_date": "2013-09-12",
        "rating": 9.5,
        "directors": "1&10",
        "genres": "4"
    })

    # then
    assert response.status_code == 201

    data = response.json
    assert data['user_id'] == 5
    assert data['directors'] == [1, 10]
    assert data['genres'] == [4]


@mock.patch("app.crud.film", new=fake_film())
def test_get_film_by_id(flask_app):
    """Checks setting UNKNOWN value, response data type and status code"""
    # when
    response = flask_app.get(url_for("api.film", film_id=5))

    # then
    assert response.status_code == 200

    data = response.json
    assert data['directors'] == 'UNKNOWN'
    assert isinstance(data, Dict)


@mock.patch("app.crud.film", new=fake_film())
def test_get_all_films(flask_app):
    """Checks setting UNKNOWN value, the number of records received and status code"""
    # when
    response = flask_app.get(
        url_for("api.films",
                page=1, per_page=5)
    )

    films = response.json

    # then
    check_count(response, code=200, count=5)
    assert (film['directors'] == 'UNKNOWN' for film in films)
