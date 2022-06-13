"""Domain base function test"""

from app import DATABASE
from app.crud import GENRE
from app.domain import delete
from app.models import Genre
from app.schemas import GenreBase


def test_delete(app_with_data):
    """Checking the correctness of the deletion"""
    before = len(DATABASE.session.query(Genre).all())
    genre = delete(GENRE, 6)
    after = len(DATABASE.session.query(Genre).all())
    assert DATABASE.session.query(Genre).get(6) is None
    assert isinstance(genre, GenreBase)
    assert after == before - 1
