"""Testing film route_domain functions"""
from typing import Dict
from unittest import mock
from flask import url_for

from app.schemas import FilmBase
from app.schemas.film import FilmList
from tests.end_to_end.endpoints.test_subfunctions import check_count


def fake_film():
    """Function for mocking"""
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

        def get_multi(self):
            """Mock get multi method"""
            films = FilmList.from_orm([self.get() for _ in range(10)])
            return films

    return FakeFilmCRUD()


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
