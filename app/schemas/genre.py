"""Module with genre pydentic schemas"""
import re
from typing import List, Optional

from pydantic import BaseModel, constr, validator


class GenreBase(BaseModel):
    """Base schema"""
    genre_name: constr(max_length=50)

    @validator("genre_name")
    def check_genre_name(cls, value):
        """Check genre name field"""
        if re.match(r'^[A-Z][a-z]*$', value) is None:
            raise ValueError("Incorrect genre name!")
        return value

    class Config:
        """Configuration class"""
        orm_mode = True


class GenreCreate(GenreBase):
    """Create schema"""


class GenreUpdate(GenreBase):
    """Update schema"""
    genre_name: Optional[constr(max_length=50)] = None


class GenreList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[GenreBase]

    class Config:
        """Configuration class"""
        orm_mode = True
