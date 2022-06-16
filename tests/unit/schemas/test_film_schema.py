"""Testing film's pydantic schema"""

from pydantic import ValidationError
import pytest

from app.schemas import FilmBase


@pytest.mark.parametrize(
    "data, valid",
    [
        ({
            "title": "Peaky Blinders",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        },
         True
        ),
        ({
            "title": "Peaky 2",
            "poster": "https://www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        },
         True
        ),
        ({
            "title": "Peaky Blinders 1",
            "poster": "www.posters.net/Peaky-Blinders-poster",
            "description": "A gangster family epic set in 1900s England.",
            "release_date": "2013-09-12",
            "rating": 9.5,
            "user_id": 4,
            "directors": [],
            "genres": []
        },
         False
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
        },
         False
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
        },
         False
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
        },
         False
        )
    ]
)
def test_validate_film(app_with_data, data, valid):
    """Checking for a validation error when entering invalid data"""
    try:
        FilmBase.parse_obj(data)
        assert valid
    except ValidationError:
        assert not valid
