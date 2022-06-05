"""Module with DIRECTOR CRUD realisation"""

from app.models import Director
from .base import CRUDBase
from app.schemas.director import DirectorCreate, DirectorUpdate, DirectorBase, DirectorList


class CRUDDirector(CRUDBase[Director, DirectorCreate, DirectorUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the DIRECTOR model"""

    ...


DIRECTOR = CRUDDirector(Director, DirectorBase, DirectorList)
