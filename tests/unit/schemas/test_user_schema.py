"""Testing user's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import UserBase


@pytest.mark.parametrize(
    "data, valid",
    [
        ({
            "role_id": 1,
            "name": "John",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }, True),
        ({
            "role_id": 1,
            "name": "john",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }, False),
        ({
            "role_id": 1,
            "name": "John",
            "email": "johny.com",
            "password": "Johny5863"
        }, False),
        ({
            "role_id": 1,
            "name": "John1",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }, False)
    ])
def test_validate_user(app_with_data, data, valid):
    """Checking for a validation error when entering invalid data"""
    try:
        UserBase.parse_obj(data)
        assert valid
    except ValidationError:
        assert not valid
