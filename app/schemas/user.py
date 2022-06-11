"""Module with user pydentic schemas"""
import re
from typing import List

from pydantic import BaseModel, EmailStr, constr, validator


class UserBase(BaseModel):
    """Base schema"""
    name: constr(max_length=50)
    email: EmailStr

    @validator("name")
    def check_name(cls, value):
        """Check name field"""
        if re.match(r'^[A-Z][a-z]*$', value) is None:
            raise ValueError("Incorrect name!")
        return value

    class Config:
        """Configuration class"""
        orm_mode = True


class UserCreate(UserBase):
    """Create schema"""
    role_id: int
    password: constr(max_length=255)


class UserUpdate(UserBase):
    """Update schema"""
    role_id: int
    password: constr(max_length=255)


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
