"""Testing user's routes"""

from flask import url_for
import pytest

from app import db, User
from app.schemas import UserBase
from loggers import logger
from .test_subfunctions import check_count


@pytest.mark.parametrize(
    "data, code",
    [
        ({
            "role_id": 1,
            "name": "Jack",
            "email": "jack@gmail.com",
            "password": "Jack895"
        }, 201),
        ({
            "role_id": 1,
            "name": "Jack",
            "email": "jacky@gmail.com",
            "password": "Jack895"
        }, 400),
        ({
            "role_id": 1,
            "name": "john",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }, 400),
        ({
            "role_id": 1,
            "name": "John",
            "email": "johny.com",
            "password": "Johny5863"
        }, 400)
    ])
def test_create_user(app_with_data, data, code):
    """
    Checking the consistency of data to create a new record,
    the status code and adding this record to the database
    """
    # when
    response = app_with_data.post(url_for("api.user_create"),
                                  json=data)

    # then
    assert response.status_code == code

    if code == 201:
        count = len(db.session.query(User).filter(User.email == data['email']).all())
        assert count == 1


@pytest.mark.parametrize(
    "user_id, code",
    [(1, 200), (4, 200), (7, 200), (25, 404), (100, 404)])
def test_get_user_by_id(app_with_data, user_id, code):
    """Checks the data received by the specified id and matches the status code"""
    # when
    response = app_with_data.get(url_for("api.user", user_id=user_id))

    # then
    assert response.status_code == code

    if code == 200:
        data = response.json
        record = UserBase.from_orm(db.session.query(User).get(user_id))
        assert data == record


@pytest.mark.parametrize(
    "user_id, data, code",
    [
        (5, {
            "role_id": 1,
            "name": "Jack",
        }, 200),
        (3, {
            "password": "Jack895"
        }, 200),
        (3, {
            "email": "jacky@gmail.com"
        }, 400),
        (25, {
            "email": "johny25@gmail.com",
            "password": "Johny5863"
        }, 404),
        (6, {
            "email": "johny.com",
        }, 400)
    ])
def test_update_user_by_id(app_with_data, user_id, data, code):
    """Checks the data after updating and matches the status code"""
    # when
    response = app_with_data.put(url_for("api.user", user_id=user_id),
                                 json=data)
    users = db.session.query(User).get(6).__dict__
    logger.info("%s", str(users))
    # then
    assert response.status_code == code
    if code == 200:
        record = UserBase.from_orm(db.session.query(User).get(user_id)).dict()
        data = response.json
        assert data == record


@pytest.mark.parametrize(
    "page, count, code",
    [(1, 10, 200), (2, 2, 200), (3, 0, 404)])
def test_get_all_users_default(app_with_data, page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.users_default",
                page=page, per_page=None)
    )

    # then
    check_count(response, code, count)


@pytest.mark.parametrize(
    "page, per_page, count, code",
    [(1, 10, 10, 200),
     (2, 1, 1, 200),
     (5, 2, 2, 200),
     (3, 5, 2, 200),
     (7, 3, 0, 404),
     (3, 6, 0, 404)
     ])
def test_get_all_users(app_with_data, page, per_page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.users", page=page, per_page=per_page)
    )

    # then
    check_count(response, code, count)


@pytest.mark.parametrize(
    "user_id, code",
    [(1, 204), (3, 204), (7, 204), (25, 404), (100, 404)])
def test_del_user_by_id(app_with_data, user_id, code):
    """Checks the status code when deleting"""
    # when
    response = app_with_data.delete(url_for("api.user", user_id=user_id))

    # then
    assert response.status_code == code
