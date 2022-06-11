"""Module with USER CRUD realisation"""

from .base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserBase, UserList


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the USER model"""
    ...


USER = CRUDUser(User, UserBase, UserList)
