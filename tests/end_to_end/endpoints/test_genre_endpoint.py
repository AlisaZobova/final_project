"""Testing genre's routes"""

from flask import url_for
import pytest

from app import DATABASE
from app.models import Genre
from app.schemas import GenreBase


@pytest.mark.parametrize(
    "data, code",
    [
        ({
            "genre_name": "Documentary"
        }, 201),
        ({
            "genre_name": "Action"
        }, 400),
        ({
            "genre_name": "documentary"
        }, 400),
        ({
            "genre_name": "DOC"
        }, 400)
    ])
def test_create_genre(app_with_data, data, code):
    """
    Checking the consistency of data to create a new record,
    the status code and adding this record to the database
    """
    # when
    response = app_with_data.post(url_for("api.genre_create"),
                                  json=data)

    # then
    assert response.status_code == code

    if code == 201:
        count = len(DATABASE.session.query(Genre)
                    .filter(Genre.genre_name == data['genre_name']).all())
        assert count == 1


@pytest.mark.parametrize(
    "genre_id, code",
    [(1, 200), (4, 200), (7, 200), (25, 404), (100, 404)])
def test_get_genre_by_id(app_with_data, genre_id, code):
    """Checks the data received by the specified id and matches the status code"""
    # when
    response = app_with_data.get(url_for("api.genre", genre_id=genre_id))

    # then
    assert response.status_code == code

    if code == 200:
        data = response.json
        record = GenreBase.from_orm(DATABASE.session.query(Genre).get(genre_id))
        assert data == record


@pytest.mark.parametrize(
    "genre_id, data, code",
    [
        (5, {
            "genre_name": "Film"
        }, 200),
        (25, {
            "genre_name": "Genre"
        }, 404),
        (6, {
            "genre_name": "Action"
        }, 400)
    ])
def test_update_genre_by_id(app_with_data, genre_id, data, code):
    """Checks the data after updating and matches the status code"""
    # when
    response = app_with_data.put(url_for("api.genre", genre_id=genre_id),
                                 json=data)

    # then
    assert response.status_code == code
    if code == 200:
        record = GenreBase.from_orm(DATABASE.session.query(Genre).get(genre_id)).dict()
        data = response.json
        assert data == record


@pytest.mark.parametrize(
    "page, count, code",
    [(1, 8, 200), (3, 0, 404)])
def test_get_all_genres_default(app_with_data, page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.genres_default",
                page=page, per_page=None)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "page, per_page, count, code",
    [(1, 10, 8, 200),
     (2, 1, 1, 200),
     (5, 2, 0, 404),
     (7, 3, 0, 404)
     ])
def test_get_all_genres(app_with_data, page, per_page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.genres", page=page, per_page=per_page)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "genre_id, code",
    [(8, 204), (7, 204), (25, 404), (100, 404)])
def test_del_genre_by_id(app_with_data, genre_id, code):
    """Checks the status code when deleting"""
    # when
    response = app_with_data.delete(url_for("api.genre", genre_id=genre_id))

    # then
    assert response.status_code == code
