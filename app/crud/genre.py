"""Module with GENRE CRUD realisation"""
from app.models import Genre, Film
from .base import CRUDBase
from app.schemas.genre import GenreCreate, GenreUpdate, GenreBase, GenreList
from app.models.db_init import DATABASE


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the GENRE model"""

    def remove(self, database: DATABASE.session, *, record_id: int) -> GenreBase:
        """Method to delete one record by id and records with it in the associative table"""
        obj = database.query(self.model).get(record_id)
        for film in database.query(Film).all():
            if film.genres.count(obj) > 0:
                film.genres.remove(obj)
        database.delete(obj)
        database.commit()
        return self.schema.from_orm(obj)


GENRE = CRUDGenre(Genre, GenreBase, GenreList)
