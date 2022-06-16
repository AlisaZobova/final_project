"""Module with USER CRUD realisation"""

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserBase, UserList
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the USER model"""
    def check_db_error(self, database, data):
        """Method for checking database errors"""
        if 'email' in data.keys():
            if len(database.query(self.model).filter(self.model.email == data['email']).all()) != 0:
                raise ValueError


USER = CRUDUser(User, UserBase, UserUpdate, UserList)
