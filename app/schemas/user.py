"""Module with user pydentic schemas"""

from typing import List

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    """Base schema"""
    name: constr(max_length=50)
    email: EmailStr

    class Config:
        """Configuration class"""
        orm_mode = True


class UserCreate(UserBase):
    """Create schema"""
    role_id: int
    password: constr(max_length=50)


class UserUpdate(UserBase):
    """Update schema"""


class UserInDBBase(UserBase):
    """Database schema"""
    user_id: int
    role_id: int


class UserList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[UserBase]

    class Config:
        """Configuration class"""
        orm_mode = True
