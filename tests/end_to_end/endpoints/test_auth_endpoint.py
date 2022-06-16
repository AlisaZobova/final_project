"""Authentication tests"""

from flask import url_for


def test_auth_no_user(app_with_db):
    """
    Checking the impossibility of authorization in the
    absence of a user with the specified email
    """
    # when
    response = app_with_db.post(
        url_for("api.authentication_login"),
        json={
            "email": "jack99@gmail.com",
            "password": "Jacky5863"
        }
    )

    # then
    assert response.status_code == 404


def test_auth(app_with_data):
    """Checks the success of authorization under normal conditions"""
    # when
    response = app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )

    # then
    assert response.status_code == 200


def test_auth_wrong_password(app_with_data):
    """Checks for authorization failure when an incorrect password entered"""
    # when
    response = app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny583"
        }
    )

    # then
    assert response.status_code == 400


def test_auth_not_enough_data_email(app_with_data):
    """
    Checks for authorization failure when entering
    insufficient data (in the absence of an email)
    """
    # when
    response = app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "password": "Johny583"
        }
    )

    # then
    assert response.status_code == 404


def test_auth_not_enough_data_password(app_with_data):
    """
    Checks for authorization failure when entering
    insufficient data (in the absence of a password)
    """
    # when
    response = app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com"
        }
    )

    # then
    assert response.status_code == 400


def test_logout(app_with_data):
    """Checks if the logout was successful if there is an authorized user"""
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )

    response = app_with_data.get(
        url_for("api.authentication_logout")
    )

    # then
    assert response.status_code == 200


def test_logout_bad(app_with_data):
    """Checks if the logout fails when there is no logged user"""
    # when
    response = app_with_data.get(
        url_for("api.authentication_logout")
    )

    # then
    assert response.status_code == 401
