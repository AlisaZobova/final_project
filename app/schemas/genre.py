"""Module with genre pydentic schemas"""

from typing import List

from pydantic import BaseModel, constr


class GenreBase(BaseModel):
    """Base schema"""
    genre_name: constr(max_length=50)

    class Config:
        """Configuration class"""
        orm_mode = True


class GenreCreate(GenreBase):
    """Create schema"""


class GenreUpdate(GenreBase):
    """Update schema"""


class GenreInDBBase(GenreBase):
    """Database schema"""
    genre_id: int


class GenreList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[GenreBase]

    class Config:
        """Configuration class"""
        orm_mode = True
