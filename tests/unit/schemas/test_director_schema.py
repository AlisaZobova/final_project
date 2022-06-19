"""Testing director's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import DirectorBase


@pytest.mark.parametrize(
    "data",
    [
        ({
            "name": "thomas",
            "surname": "Shelby"
        }),
        ({
            "name": "Thomas",
            "surname": "shelby"
        }),
        ({
            "name": "4",
            "surname": "Shelby"
        }),
        ({
            "name": "Thomas",
            "surname": "4"
        })
    ])
def test_validate_director(data):
    """Checking for a validation error when entering invalid data"""
    with pytest.raises(ValidationError):
        DirectorBase.parse_obj(data)
