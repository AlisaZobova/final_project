"""Module with director CRUD realisation"""

from app.models import Director, Film
from app.schemas.director import DirectorCreate, DirectorUpdate, DirectorBase, DirectorList
from .base import CRUDBase


class CRUDDirector(CRUDBase[Director, DirectorCreate, DirectorUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the director model"""

    def remove(self, *, record_id: int) -> DirectorBase:
        """Method to delete one record by id and records with it in the associative table"""
        obj = self.database.query(self.model).get(record_id)
        for film in self.database.query(Film).all():
            if film.directors.count(obj) > 0:
                film.directors.remove(obj)
        self.database.delete(obj)
        self.database.commit()
        return self.schema.from_orm(obj)


director = CRUDDirector(Director, DirectorBase, DirectorUpdate, DirectorList)
