"""Testing genre's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import GenreBase


@pytest.mark.parametrize(
    "data",
    [
        ({
            "genre_name": 25
        }),
        ({
            "genre_name": "comedy"
        }),
        ({
            "genre_name": "Comedy2"
        })
    ])
def test_validate_genre(data):
    """Checking for a validation error when entering invalid data"""
    with pytest.raises(ValidationError):
        GenreBase.parse_obj(data)
