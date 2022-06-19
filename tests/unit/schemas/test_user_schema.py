"""Testing user's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import UserBase


@pytest.mark.parametrize(
    "data",
    [
        ({
            "role_id": 1,
            "name": "john",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }),
        ({
            "role_id": 1,
            "name": "John",
            "email": "johny.com",
            "password": "Johny5863"
        }),
        ({
            "role_id": 1,
            "name": "John1",
            "email": "johny@gmail.com",
            "password": "Johny5863"
        }),
        ({
            "role_id": 1,
            "name": "John",
            "email": "johnyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy@gmail.com",
            "password": "Johny5863"
        })
    ])
def test_validate_user(data):
    """Checking for a validation error when entering invalid data"""
    with pytest.raises(ValidationError):
        UserBase.parse_obj(data)
