"""Testing film's routes"""

from flask import url_for
import pytest

from app import DATABASE
from app.domain import set_unknown_director
from app.models import Film
from app.schemas import FilmBase


@pytest.mark.parametrize(
    "data",
    {
        "title": "Jacky",
        "poster": "https://www.posters.net/Peaky-Blinders-poster",
        "description": "A gangster family epic set in 1900s England.",
        "release_date": "2013-09-12",
        "rating": 9.5,
        "user_id": 4,
        "directors": "1&10",
        "genres": "4"
    })
def test_create_film_no_auth(app_with_data, data):
    """Checking that it is not possible to create a film without prior authentication"""
    # when
    response = app_with_data.post(url_for("api.film_create"),
                                  json=data)

    # then
    assert response.status_code == 401


@pytest.mark.parametrize(
    "data, code",
    [
        ({
            "title": "Jacky",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": "1&10",
            "genres": "4"
        },
         201
        ),
        ({
            "title": "History",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 7.6,
            "user_id": 4,
            "directors": "2",
            "genres": "4"
        },
         201),
        ({
            "title": "jacky",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": "1&10",
            "genres": "4"
        },
         400
        ),
        ({
            "title": "Jacky",
            "poster": "www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": "1&10",
            "genres": "4"
        },
         400
        ),
        ({
            "title": "Jacky",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2033-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": "1&10",
            "genres": "4"
        },
         400
        )
    ]
)
def test_create_film_auth(app_with_data, data, code):
    """
    Checking the consistency of data to create a new record,
    the status code and adding this record to the database
    if there is an authorized user
    """
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )
    response = app_with_data.post(url_for("api.film_create"),
                                  json=data)

    # then
    assert response.status_code == code

    if code == 201:
        count = len(DATABASE.session.query(Film).filter(Film.title == data['title']).all())
        assert count == 1

    app_with_data.get(
        url_for("api.authentication_logout")
    )


def test_create_film_duplicate(app_with_data):
    """Checking the impossibility of creating a film with a duplicate title """
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )
    data = {
        "title": "Jacky",
        "poster": "https://www.posters.net/Peaky-Blinders-poster",
        "description": "A gangster family epic set in 1900s England.",
        "release_date": "2013-09-12",
        "rating": 9.5,
        "user_id": 4,
        "directors": "1&10",
        "genres": "4"
    }

    app_with_data.post(url_for("api.film_create"), json=data)

    response = app_with_data.post(url_for("api.film_create"), json=data)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "film_id, code",
    [(1, 200), (4, 200), (2, 200), (25, 404), (100, 404)])
def test_get_film_by_id(app_with_data, film_id, code):
    """Checks the data received by the specified id and matches the status code"""
    # when
    response = app_with_data.get(url_for("api.film", film_id=film_id))

    # then
    assert response.status_code == code

    if code == 200:
        data = response.json
        record = FilmBase.from_orm(DATABASE.session.query(Film).get(film_id)).dict()
        assert data == set_unknown_director(record)


@pytest.mark.parametrize(
    "film_id, data",
    [(5, {
        "description": "Super film."
    })])
def test_update_film_by_id_no_auth(app_with_data, data, film_id):
    """Checking that a film cannot be updated by an unauthenticated user"""
    # when
    response = app_with_data.put(url_for("api.film", film_id=film_id),
                                 json=data)

    # then
    assert response.status_code == 401


@pytest.mark.parametrize(
    "film_id, data",
    [(5, {
        "description": "Super film."
    })])
def test_update_film_by_id_bad_auth(app_with_data, film_id, data):
    """
    Verifying that a film cannot be updated by a user
    who did not create this movie and is not an administrator
    """
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "jacky@gmail.com",
            "password": "Jacky"
        }
    )
    response = app_with_data.put(url_for("api.film", film_id=film_id),
                                 json=data)

    # then
    assert response.status_code == 403

    app_with_data.get(
        url_for("api.authentication_logout")
    )


@pytest.mark.parametrize(
    "film_id, data, code",
    [
        (5, {
            "description": "Super film."
        }, 200),
        (4, {
            "title": "Film"
        }, 200),
        (3, {
            "poster": "poster"
        }, 400),
        (25, {
            "title": "Genre"
        }, 404),
        (5, {
            "title": "Mary Johnson"
        }, 400)
    ])
def test_update_film_by_id_auth(app_with_data, film_id, data, code):
    """
    Checks the data after updating and matches the status code
    if there is a right authorized user
    """
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )
    response = app_with_data.put(url_for("api.film", film_id=film_id),
                                 json=data)

    # then
    assert response.status_code == code
    if code == 200:
        record = FilmBase.from_orm(DATABASE.session.query(Film).get(film_id)).dict()

        data = response.json
        assert data == set_unknown_director(record)

    app_with_data.get(
        url_for("api.authentication_logout")
    )


@pytest.mark.parametrize(
    "page, count, code",
    [(1, 5, 200), (2, 0, 404)])
def test_get_all_films_default(app_with_data, page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_default",
                page=page, per_page=None)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "page, per_page, count, code",
    [(1, 10, 5, 200),
     (2, 1, 1, 200),
     (5, 2, 0, 404)
     ])
def test_get_all_films(app_with_data, page, per_page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films", page=page, per_page=per_page)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "title, page, count, code",
    [("Mar", 1, 2, 200), ("Evening", 1, 1, 200), ("other", 1, 1, 200)
     ])
def test_get_all_films_by_title_default(app_with_data, title, page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_title_default",
                title=title, page=page, per_page=None)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "title, page, per_page, count, code",
    [("Mar", 1, 2, 2, 200), ("Mar", 1, 1, 1, 200)
     ])
def test_get_all_films_by_title(app_with_data, title, page, per_page, count, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_title", title=title, page=page, per_page=per_page)
    )

    # then
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count


@pytest.mark.parametrize(
    "page, order, code",
    [(1, ['asc', None], 200), (1, ['desc', 'asc'], 200),
     (1, [None, 'desc'], 200), (5, [None, 'desc'], 404)])
def test_get_all_films_sorted_default(app_with_data, page, order, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_sort_default",
                order=order, page=page, per_page=None)
    )

    # then
    assert response.status_code == code


@pytest.mark.parametrize(
    "page, per_page, order, code",
    [(1, 1, ['asc', None], 200), (2, 2, ['desc', 'asc'], 200), (2, 3, [None, 'desc'], 200),
     (2, 10, [None, 'desc'], 404)
     ])
def test_get_all_films_sorted(app_with_data, page, per_page, order, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_sort", order=order, page=page, per_page=per_page)
    )

    # then
    assert response.status_code == code


@pytest.mark.parametrize(
    "page, data, code",
    [(1, ["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 200),
     (5, ["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 404)])
def test_get_all_films_filtered_default(app_with_data, page, data, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_filter_default",
                data=data, page=page, per_page=None)
    )

    # then
    assert response.status_code == code


@pytest.mark.parametrize(
    "page, per_page, data, code",
    [(1, 1, ["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 200),
     (2, 1, ["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 200),
     (5, 10, ["2001-2020", "Jack_Jackson", 'Fantasy&Drama'], 404)
     ])
def test_get_all_films_filtered(app_with_data, page, per_page, data, code):
    """Checks the number of records received and status code"""
    # when
    response = app_with_data.get(
        url_for("api.films_filter", data=data, page=page, per_page=per_page)
    )

    # then
    assert response.status_code == code


def test_delete_film_by_id_no_auth(app_with_data):
    """Checking that a film cannot be deleted by an unauthenticated user"""
    # when
    response = app_with_data.delete(url_for("api.film", film_id=6))

    # then
    assert response.status_code == 401


def test_delete_film_by_id_bad_auth(app_with_data):
    """
    Verifying that a film cannot be deleted by a user
    who did not create this movie and is not an administrator
    """
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "jacky@gmail.com",
            "password": "Jacky"
        }
    )
    response = app_with_data.delete(url_for("api.film", film_id=5))

    # then
    assert response.status_code == 403

    app_with_data.get(
        url_for("api.authentication_logout")
    )


@pytest.mark.parametrize(
    "film_id, code",
    [(4, 204), (5, 204), (25, 404), (100, 404)])
def test_del_film_by_id_auth(app_with_data, film_id, code):
    """
    Checks the status code when deleting
    if there is a right authorized user
    """
    # when
    app_with_data.post(
        url_for("api.authentication_login"),
        json={
            "email": "john@gmail.com",
            "password": "Johny5863"
        }
    )
    response = app_with_data.delete(url_for("api.film", film_id=film_id))

    # then
    assert response.status_code == code

    app_with_data.get(
        url_for("api.authentication_logout")
    )
