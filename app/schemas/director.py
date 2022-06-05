"""Module with director pydentic schemas"""

from typing import List

from pydantic import BaseModel, constr


class DirectorBase(BaseModel):
    """Base schema"""
    name: constr(max_length=50)
    surname: constr(max_length=50)

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
