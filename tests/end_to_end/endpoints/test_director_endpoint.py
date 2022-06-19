"""Testing director's routes"""

from flask import url_for
import pytest

from app import db
from app.models import Director
from app.schemas import DirectorBase
from .test_subfunctions import check_count


@pytest.mark.parametrize(
    "data, code",
    [
        ({
            "name": "Johny",
            "surname": "Frank"
        }, 201),
        ({
            "name": "johny",
            "surname": "Frank"
        }, 400),
        ({
            "name": "Johny",
            "surname": "4rank"
        }, 400)
    ])
def test_create_director(app_with_data, data, code):
    """
    Checking the consistency of data to create a new record,
    the status code and adding this record to the database
    """
    # when
    count_before = len(db.session.query(Director)
                       .filter((Director.name == data['name']) &
                               (Director.surname == data['surname'])).all())
    response = app_with_data.post(url_for("api.director_create"), json=data)

    # then
    assert response.status_code == code

    if code == 201:
        count = len(db.session.query(Director)
                    .filter((Director.name == data['name']) &
                            (Director.surname == data['surname'])).all())
        assert count == count_before + 1


@pytest.mark.parametrize(
    "director_id, code",
    [(1, 200), (4, 200), (7, 200), (25, 404), (100, 404)])
def test_get_director_by_id(app_with_data, director_id, code):
    """Checks the data received by the specified id and matches the status code"""
    # when
    response = app_with_data.get(url_for("api.director", director_id=director_id))

    # then
    assert response.status_code == code

    if code == 200:
        data = response.json
        record = DirectorBase.from_orm(db.session.query(Director).get(director_id))
        assert data == record


@pytest.mark.parametrize(
    "director_id, data, code",
    [
        (5, {
            "name": "Jack",
        }, 200),
        (3, {
            "surname": "Valla"
        }, 200),
        (25, {
            'name': 'Var'
        }, 404),
        (6, {
            'name': "fill",
        }, 400)
    ])
def test_update_director_by_id(app_with_data, director_id, data, code):
    """Checks the data after updating and matches the status code"""
    # when
    response = app_with_data.put(url_for("api.director", director_id=director_id), json=data)
    # then
    assert response.status_code == code

    if code == 200:
        record = DirectorBase.from_orm(db.session.query(Director).get(director_id)).dict()
        data = response.json
        assert data == record


@pytest.mark.parametrize(
    "page, count, code",
    [(1, 10, 200), (2, 2, 200), (3, 0, 404)])
def test_get_all_directors_default(app_with_data, page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.directors_default", page=page, per_page=None)
    )

    # then
    check_count(response, code, count)


@pytest.mark.parametrize(
    "page, per_page, count, code",
    [(1, 10, 10, 200),
     (2, 1, 1, 200),
     (5, 2, 2, 200),
     (7, 3, 0, 404)
     ])
def test_get_all_directors(app_with_data, page, per_page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.directors", page=page, per_page=per_page)
    )

    # then
    check_count(response, code, count)


@pytest.mark.parametrize(
    "director_id, code",
    [(8, 204), (9, 204), (25, 404), (100, 404)])
def test_del_director_by_id(app_with_data, director_id, code):
    """Checks the status code when deleting"""
    # when
    response = app_with_data.delete(url_for("api.director", director_id=director_id))

    # then
    assert response.status_code == code
