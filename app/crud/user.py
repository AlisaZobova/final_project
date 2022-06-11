"""Module with USER CRUD realisation"""
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash

from .base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserBase, UserList
from app.models.db_init import DATABASE


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the USER model"""
    def create(self, database: DATABASE.session, obj_in: Union[UserCreate, Dict[str, Any]],
               **kwargs) -> UserBase:
        """Method to create one record"""
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = generate_password_hash(obj_in_data['password'], method='sha256')
        database_obj = self.model(**obj_in_data)
        user = self.schema.from_orm(database_obj)
        database.add(database_obj)
        database.commit()
        database.refresh(database_obj)
        return user


USER = CRUDUser(User, UserBase, UserList)
