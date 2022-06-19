"""Module with genre CRUD realisation"""
from typing import Dict, Any

from app.models import Genre, Film
from app.schemas.genre import GenreCreate, GenreUpdate, GenreBase, GenreList
from .base import CRUDBase


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the genre model"""
    def check_db_error(self, data: Dict[str, Any]):
        """Method for checking genre name duplicates"""
        if 'genre_name' in data.keys():
            if len(self.database.query(self.model)
                   .filter(self.model.genre_name == data['genre_name']).all()) != 0:
                raise ValueError

    def remove(self, *, record_id: int) -> GenreBase:
        """Method to delete one record by id and records with it in the associative table"""
        obj = self.database.query(self.model).get(record_id)
        for film in self.database.query(Film).all():
            if film.genres.count(obj) > 0:
                film.genres.remove(obj)
        self.database.delete(obj)
        self.database.commit()
        return self.schema.from_orm(obj)


genre = CRUDGenre(Genre, GenreBase, GenreUpdate, GenreList)
