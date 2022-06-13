"""Module with GENRE CRUD realisation"""

from app.models import Genre, Film
from app.schemas.genre import GenreCreate, GenreUpdate, GenreBase, GenreList
from app.models.db_init import DATABASE
from .base import CRUDBase


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the GENRE model"""
    def check_db_error(self, database, data):
        """Method for checking database errors"""
        if 'genre_name' in data.keys():
            if len(database.query(self.model)
                   .filter(self.model.genre_name == data['genre_name']).all()) != 0:
                raise ValueError

    def remove(self, database: DATABASE.session, *, record_id: int) -> GenreBase:
        """Method to delete one record by id and records with it in the associative table"""
        obj = database.query(self.model).get(record_id)
        for film in database.query(Film).all():
            if film.genres.count(obj) > 0:
                film.genres.remove(obj)
        database.delete(obj)
        database.commit()
        return self.schema.from_orm(obj)


GENRE = CRUDGenre(Genre, GenreBase, GenreUpdate, GenreList)
