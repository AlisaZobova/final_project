"""Models module"""

from sqlalchemy import Table, Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Role(Base):
    """Class to store user roles"""
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    users = relationship('User', backref='role')


class User(Base):
    """Class to store users and information about them"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.role_id'), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


film_director = Table(
    "film_director",
    Base.metadata,
    Column("film_id", ForeignKey("film.film_id"), primary_key=True),
    Column("director_id", ForeignKey("director.director_id"), primary_key=True),
)


film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("film.film_id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.genre_id"), primary_key=True),
)


class Film(Base):
    """Class to store films and information about them"""
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    poster = Column(String(50), nullable=False)
    description = Column(Text)
    release_date = Column(Date, nullable=False)
    rating = Column(Float, nullable=False)
    directors = relationship("Director", secondary=film_director, backref="films")
    genres = relationship("Genre", secondary=film_genre, backref="films")


class Director(Base):
    """Class to store directors and information about them"""
    __tablename__ = 'director'
    director_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)


class Genre(Base):
    """Class to store genres"""
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(50), unique=True)
