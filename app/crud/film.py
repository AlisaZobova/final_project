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

    def query_film_filter(
            self, database: DATABASE.session, column_name: str,
            value: str, page=1, per_page=10
    ):
        """Method for filtering records by release_date or genres or directors"""
        if column_name == 'release_date':
            start_year, end_year = value.split('-')
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 self.query_paginate(
                     self.multy_query(database).filter(extract('year', self.model.release_date)
                                                       .between(start_year, end_year))
                     .order_by(self.model.film_id.asc()), page=page, per_page=per_page)])
        if column_name == 'genres':
            genres_names = value.split('&')
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 self.query_paginate(
                     self.multy_query(database).distinct().filter(
                         or_(*[self.model.genres
                               .contains(genre) for genre in database.query(Genre).filter(
                                   Genre.genre_name.in_(genres_names)).all()])),
                     page=page, per_page=per_page)])
        if column_name == 'directors':
            directors_names = value.split('&')
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 self.query_paginate(
                     self.multy_query(database).filter(
                         or_(*[self.model.directors
                               .contains(director) for director in database.query(Director).filter(
                                   ((Director.name + '_' + Director.surname)
                                    .in_(directors_names))).all()])),
                     page=page, per_page=per_page)])

        return None

    def query_film_sort(
            self, database: DATABASE.session, column_name: str,
            page=1, per_page=10, order: str = 'asc'
    ):
        """Method for sorting records by release_date or rating"""
        if column_name in ['rating', 'release_date']:
            if order == 'asc':
                return self.list_schema.from_orm(
                    [self.schema.from_orm(item) for item in
                     self.query_paginate(
                         self.multy_query(database).order_by(
                             self.model.__table__.columns[column_name].asc()),
                         page=page, per_page=per_page)])
            if order == 'desc':
                return self.list_schema.from_orm(
                    [self.schema.from_orm(item) for item in
                     self.query_paginate(
                         self.multy_query(database).order_by(
                             self.model.__table__.columns[column_name].desc()),
                         page=page, per_page=per_page)])

        return None

    def query_film_multy_filter(
            self, database: DATABASE.session,
            values: List[str], page=1, per_page=10
    ):
        """Method for filtering records by genres, release_date and directors"""
        genres_names = values[0].split('&')
        start_year, end_year = values[1].split('-')
        directors_names = values[2].split('&')
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in database.query(Film)
             .join(Genre, Film.genres)
             .join(Director, Film.directors)
             .filter(
                 or_(*[self.model.genres
                       .contains(genre) for genre in database.query(Genre).filter(
                           Genre.genre_name.in_(genres_names)).all()]))
             .filter(extract('year', self.model.release_date)
                     .between(start_year, end_year))
             .filter(
                 or_(*[self.model.directors
                       .contains(director) for director in database.query(Director).filter(
                           ((Director.name + '_' + Director.surname)
                            .in_(directors_names))).all()]))
             .order_by(self.model.film_id.asc())
             .paginate(page=page, per_page=per_page).items]
        )

    def query_film_multy_sort(
            self, database: DATABASE.session, page=1,
            per_page=10, order: str = 'asc'
    ):
        """Method for sorting records by release_date and rating"""
        if order == 'asc':
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 self.query_paginate(
                     self.multy_query(database).order_by(
                         self.model.release_date.asc(), self.model.rating.asc()),
                     page=page, per_page=per_page)])
        if order == 'desc':
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 self.query_paginate(
                     self.multy_query(database).order_by(
                         self.model.release_date.desc(), self.model.rating.desc()),
                     page=page, per_page=per_page)])

        return None


FILM = CRUDFilm(Film, FilmBase, FilmList)
