"""Module with FILM CRUD realisation"""

from typing import List, Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract, or_

from app.models import Genre, Director, Film
from app.schemas.film import FilmCreate, FilmUpdate, FilmBase, FilmList
from app.models.db_init import DATABASE
from .base import CRUDBase
from .film_base import FilmAbstract


class CRUDFilm(CRUDBase[Film, FilmCreate, FilmUpdate], FilmAbstract):
    """A class that inherits the base self class and implements
    own methods to perform self operations for the FILM model"""

    def create(self, database: DATABASE.session, obj_in:
               Union[FilmCreate, Dict[str, Any]], **kwargs) -> FilmBase:
        """Method to create one record"""
        directors = kwargs['directors']
        genres = kwargs['genres']
        obj_in_data = jsonable_encoder(obj_in)
        database_obj = self.model(**obj_in_data)
        for genre in genres:
            database_obj.genres.append(genre)
        for director in directors:
            database_obj.directors.append(director)
        database.add(database_obj)
        database.commit()
        database.refresh(database_obj)
        return self.schema.from_orm(database_obj)

    def multy_query(self, database: DATABASE.session):
        """Method for creating multy queries"""
        return database.query(self.model)

    def query_paginate(self, query, page: int = 1, per_page: int = 10):
        """Method for pagination multy queries"""
        return query.paginate(page=page, per_page=per_page).items

    def get_multi(
            self, database: DATABASE.session, *,
            page=1, per_page: int = 10
    ) -> List[FilmBase]:
        """Method to read all records from a table with default pagination set to 10"""
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in
             self.query_paginate(
                 self.multy_query(database)
                 .order_by(self.model.film_id.asc()),
                 page=page, per_page=per_page)])

    def get_multi_by_title(
            self, database: DATABASE.session, title: str, page=1, per_page: int = 10
    ) -> List[FilmBase]:
        """A method that searches for a partial match of a movie title"""
        title = f'%{title}%'
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in
             self.query_paginate(
                 self.multy_query(database)
                 .filter(self.model.title.ilike(title))
                 .order_by(self.model.film_id.asc()), page=page, per_page=per_page)])

    def date_filter(self, query, value):
        """Method for filtering by release date"""
        start_year, end_year = value.split('-')
        return query.filter(extract('year', self.model.release_date)
                         .between(start_year, end_year))

    def director_filter(self, query, value, database):
        """Method for filtering by directors"""
        directors_names = value.split('&')
        return query.filter(
                     or_(*[self.model.directors
                           .contains(director) for director in database.query(Director).filter(
                               ((Director.name + '_' + Director.surname)
                                .in_(directors_names))).all()]))

    def genre_filter(self, query, value, database):
        """Method for filtering by genres"""
        genres_names = value.split('&')
        return query.filter(
                    or_(*[self.model.genres
                        .contains(genre) for genre in database.query(Genre).filter(
                        Genre.genre_name.in_(genres_names)).all()]))

    def query_film_multy_filter(
            self, database: DATABASE.session,
            values: List[str], page=1, per_page=10
    ):
        """Method for filtering records by genres, release_date and directors"""
        query = database.query(self.model).distinct()

        if values[0] is not None:
            query = self.date_filter(query=query, value=values[0])
        if values[1] is not None:
            query.join(Director, Film.directors)
            query = self.director_filter(query=query, value=values[1], database=database)
        if values[2] is not None:
            query.join(Genre, Film.genres)
            query = self.genre_filter(query=query, value=values[2], database=database)

        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in query
             .order_by(self.model.film_id.asc())
             .paginate(page=page, per_page=per_page).items])

    def date_asc(self, query):
        """Method to sort by date in ascending order"""
        return query.order_by(self.model.release_date.asc())

    def date_desc(self, query):
        """Method to sort by date in descending order"""
        return query.order_by(self.model.release_date.desc())

    def rating_asc(self, query):
        """Method to sort by rating in ascending order"""
        return query.order_by(self.model.rating.asc())

    def rating_desc(self, query):
        """Method to sort by rating in descending order"""
        return query.order_by(self.model.rating.desc())

    def query_film_multy_sort(
            self, database: DATABASE.session, order: List[str],
            page: int = 1, per_page: int = 10
    ):
        """Method for sorting records by release_date and rating"""
        query = self.multy_query(database)

        if order[0] is not None:
            if order[0] == 'asc':
                query = self.date_asc(query)
            if order[0] == 'desc':
                query = self.date_desc(query)

        if order[1] is not None:
            if order[1] == 'asc':
                query = self.rating_asc(query)
            if order[1] == 'desc':
                query = self.rating_desc(query)

        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in
             self.query_paginate(query, page=page, per_page=per_page)])


FILM = CRUDFilm(Film, FilmBase, FilmList)
