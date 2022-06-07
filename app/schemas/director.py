"""Module with director pydentic schemas"""
import re
from typing import List

from pydantic import BaseModel, constr, validator


class DirectorBase(BaseModel):
    """Base schema"""
    name: constr(max_length=50)
    surname: constr(max_length=50)

    @validator("name")
    def check_name(cls, value):
        """Check name field"""
        if re.match(r'^[A-Z][a-z]*$', value) is None:
            raise ValueError("Incorrect name!")
        return value

    @validator("surname")
    def check_surname(cls, value):
        """Check surname field"""
        if re.match(r'^[A-Z][a-z]*$', value) is None:
            raise ValueError("Incorrect surname!")
        return value

    class Config:
        """Configuration class"""
        orm_mode = True


class DirectorCreate(DirectorBase):
    """Create schema"""


class DirectorUpdate(DirectorBase):
    """Update schema"""


class DirectorInDBBase(DirectorBase):
    """Database schema"""
    director_id: int


class DirectorList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[DirectorBase]

    class Config:
        """Configuration class"""
        orm_mode = True
