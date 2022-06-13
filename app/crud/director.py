"""Module with DIRECTOR CRUD realisation"""

from app.models import Director, Film
from app.schemas.director import DirectorCreate, DirectorUpdate, DirectorBase, DirectorList
from app.models.db_init import DATABASE
from .base import CRUDBase


class CRUDDirector(CRUDBase[Director, DirectorCreate, DirectorUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the DIRECTOR model"""

    def remove(self, database: DATABASE.session, *, record_id: int) -> DirectorBase:
        """Method to delete one record by id and records with it in the associative table"""
        obj = database.query(self.model).get(record_id)
        for film in database.query(Film).all():
            if film.directors.count(obj) > 0:
                film.directors.remove(obj)
        database.delete(obj)
        database.commit()
        return self.schema.from_orm(obj)


DIRECTOR = CRUDDirector(Director, DirectorBase, DirectorUpdate, DirectorList)
