"""Testing genre's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import GenreBase


@pytest.mark.parametrize(
    "data, valid",
    [
        ({
            "genre_name": "Comedy"
        }, True),
        ({
            "genre_name": 25
        }, False),
        ({
            "genre_name": "comedy"
        }, False),
        ({
            "genre_name": "Comedy2"
        }, False)
    ])
def test_validate_user(app_with_db, data, valid):
    """Checking for a validation error when entering invalid data"""
    try:
        GenreBase.parse_obj(data)
        assert valid
    except ValidationError:
        assert not valid
