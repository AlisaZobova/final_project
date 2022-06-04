"""Module with GENRE CRUD realisation"""
from app.models import Genre
from .base import CRUDBase
from app.schemas.genre import GenreCreate, GenreUpdate, GenreBase, GenreList


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the GENRE model"""

    ...


GENRE = CRUDGenre(Genre, GenreBase, GenreList)
