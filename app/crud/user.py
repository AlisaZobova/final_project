"""Module with user CRUD realisation"""

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserBase, UserList
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the user model"""
    def check_db_error(self, data):
        """Method for checking email duplicates"""
        if 'email' in data.keys():
            if len(self.database.query(self.model)
                   .filter(self.model.email == data['email']).all()) != 0:
                raise ValueError


user = CRUDUser(User, UserBase, UserUpdate, UserList)
