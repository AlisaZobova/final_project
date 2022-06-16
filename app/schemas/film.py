"""Module with film pydentic schemas"""
import re
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, constr, confloat, validator

from .genre import GenreBase
from .director import DirectorBase


class FilmBase(BaseModel):
    """Base schema"""
    title: constr(max_length=50)
    poster: HttpUrl
    release_date: date
    rating: confloat(ge=0, le=10)
    directors: List[DirectorBase]
    genres: List[GenreBase]

    @validator("release_date")
    def check_date(cls, value):
        """Check date field"""
        if value > date.today():
            raise ValueError("The date has not yet arrived!")
        return value

    @validator("title")
    def check_title(cls, value):
        """Check title field"""
        if re.match(r'^[A-Z][a-z]*(\s(([A-Z][a-z]*)|([a-z]+)))*(\s[0-9]+)*$', value) is None:
            raise ValueError("Incorrect title!")
        return value

    class Config:
        """Configuration class"""
        orm_mode = True


class FilmCreate(FilmBase):
    """Create schema"""
    user_id: int


class FilmUpdate(FilmBase):
    """Update schema"""
    title: Optional[constr(max_length=50)] = None
    poster: Optional[HttpUrl] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[confloat(ge=0, le=10)] = None
    directors: Optional[List[DirectorBase]] = None
    genres: Optional[List[GenreBase]] = None


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
