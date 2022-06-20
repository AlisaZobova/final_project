"""Module with director pydentic schemas"""
import re
from typing import List, Optional

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
    name: Optional[constr(max_length=50)] = None
    surname: Optional[constr(max_length=50)] = None


class DirectorList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[DirectorBase]

    class Config:
        """Configuration class"""
        orm_mode = True
