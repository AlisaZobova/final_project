"""Module with user pydentic schemas"""
import re
from typing import List, Optional

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

    @validator("email")
    def check_email(cls, value):
        """Check email field"""
        if len(value) > 50:
            raise ValueError("Too long email!")
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
    role_id: Optional[int] = None
    name: Optional[constr(max_length=50)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(max_length=255)] = None


class UserList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[UserBase]

    class Config:
        """Configuration class"""
        orm_mode = True
