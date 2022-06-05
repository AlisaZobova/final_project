"""Module with film pydentic schemas"""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, constr, confloat

from .genre import GenreBase
from .director import DirectorBase


class FilmBase(BaseModel):
    """Base schema"""
    title: constr(max_length=50)
    poster: HttpUrl
    description: Optional[str] = None
    release_date: date
    rating: confloat(ge=0, le=10)
    directors: List[DirectorBase]
    genres: List[GenreBase]

    class Config:
        """Configuration class"""
        orm_mode = True


class FilmCreate(FilmBase):
    """Create schema"""
    user_id: int


class FilmUpdate(FilmBase):
    """Update schema"""


class FilmInDBBase(FilmBase):
    """Database schema"""
    film_id: int
    user_id: int


class FilmList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[FilmBase]

    class Config:
        """Configuration class"""
        orm_mode = True
