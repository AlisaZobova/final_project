"""Testing film's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import FilmBase


@pytest.mark.parametrize(
    "data",
    [
        ({
            "title": "Peaky Blinders 1",
            "poster": "www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        }
        ),
        ({
            "title": "peaky Blinders",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        }
        ),
        ({
            "title": "Peaky124",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        }
        ),
        ({
            "title": "Peaky Blinders 2",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2025-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        }
        ),
        ({
            "title": "Peaky Blinders",
            "poster": "https://www.posters.net/Peaky-Blinders-poster/yyyyyyyyyyyyyyyyyyyyyyy"
                      "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        }
        )
    ]
)
def test_validate_film(data):
    """Checking for a validation error when entering invalid data"""
    with pytest.raises(ValidationError):
        FilmBase.parse_obj(data)
