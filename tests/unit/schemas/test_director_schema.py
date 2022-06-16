"""Testing director's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import DirectorBase


@pytest.mark.parametrize(
    "data, valid",
    [
        ({
            "name": "Thomas",
            "surname": "Shelby"
        }, True),
        ({
            "name": "thomas",
            "surname": "Shelby"
        }, False),
        ({
            "name": "Thomas",
            "surname": "shelby"
        }, False),
        ({
            "name": "4",
            "surname": "Shelby"
        }, False),
        ({
            "name": "Thomas",
            "surname": "4"
        }, False)
    ])
def test_validate_user(app_with_db, data, valid):
    """Checking for a validation error when entering invalid data"""
    try:
        DirectorBase.parse_obj(data)
        assert valid
    except ValidationError:
        assert not valid
