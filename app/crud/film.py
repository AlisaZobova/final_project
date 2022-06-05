"""Module with FILM CRUD realisation"""

from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract
from sqlalchemy.orm import joinedload

from .base import CRUDBase
from .film_base import FilmAbstract
from app.models import Genre, Director, Film
from app.schemas.film import FilmCreate, FilmUpdate, FilmBase, FilmList
from app.models.db_init import DATABASE


class CRUDFilm(CRUDBase[Film, FilmCreate, FilmUpdate], FilmAbstract):
    """A class that inherits the base self class and implements
    own methods to perform self operations for the FILM model"""
    def get(self, database: DATABASE.session, record_id: Any) -> [FilmBase]:
        """Method to read one record by id"""
        return self.schema.from_orm(database.query(Film).options(
            joinedload(Film.genres), joinedload(Film.directors)).get(record_id))

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

    def get_multi(
            self, database: DATABASE.session, *,
            page=1, per_page: int = 10
    ) -> List[FilmBase]:
        """Method to read all records from a table with default pagination set to 10"""
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in database.query(self.model).options(
                joinedload(Film.genres), joinedload(Film.directors)).paginate(
                    page=page, per_page=per_page).items])

    def get_multi_by_title(
            self, database: DATABASE.session, title: str, page=1, per_page: int = 10
    ) -> List[FilmBase]:
        """A method that searches for a partial match of a movie title"""
        title = f'%{title}%'
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in database.query(
                self.model).filter(self.model.title.ilike(title)).options(
                joinedload(Film.genres), joinedload(Film.directors)).paginate(
                    page=page, per_page=per_page).items])

    def query_film_filter(
            self, database: DATABASE.session, column_name: str,
            value: str, page=1, per_page=10
    ):
        """Method for filtering records by release_date or genres or directors"""
        if column_name == 'release_date':
            start_year, end_year = value.split('-')
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 database.query(self.model).filter(extract(
                     'year', self.model.__table__.columns[column_name]).between(
                         start_year, end_year)).paginate(page=page, per_page=per_page).items])
        if column_name == 'genres':
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 database.query(self.model).filter(
                     self.model.genres.contains(database.query(Genre).filter(
                         Genre.genre_name == value).first())).paginate(
                             page=page, per_page=per_page).items])
        if column_name == 'directors':
            name, surname = value.split(' ')
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 database.query(self.model).filter(
                     self.model.directors.contains(database.query(Director).filter(
                         (Director.name == name) &
                         (Director.surname == surname)).first())).paginate(
                             page=page, per_page=per_page).items])

        return None

    def query_film_sort(
            self, database: DATABASE.session, column_name: str,
            page=1, per_page=10, order: str = 'ASC'
    ):
        """Method for sorting records by release_date or rating"""
        if column_name in ['rating', 'release_date']:
            if order == 'ASC':
                return self.list_schema.from_orm(
                    [self.schema.from_orm(item) for item in
                     database.query(self.model).order_by(
                         self.model.__table__.columns[column_name].asc()
                     ).paginate(page=page, per_page=per_page).items])
            if order == 'DESC':
                return self.list_schema.from_orm(
                    [self.schema.from_orm(item) for item in
                     database.query(self.model).order_by(
                         self.model.__table__.columns[column_name].desc()
                     ).paginate(page=page, per_page=per_page).items])

        return None

    def query_film_multy_filter(
            self, database: DATABASE.session,
            values: List[str], page=1, per_page=10
    ):
        """Method for filtering records by genres, release_date and directors"""
        start_year, end_year = values[1].split('-')
        name, surname = values[2].split('_')
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in database.query(Film)
             .join(Genre, Film.genres)
             .join(Director, Film.directors)
             .filter(Genre.genre_name == values[0])
             .filter(extract('year', self.model.release_date)
                     .between(start_year, end_year))
             .filter((Director.name == name) &
                     (Director.surname == surname))
             .paginate(page=page, per_page=per_page).items]
        )

    def query_film_multy_sort(
            self, database: DATABASE.session, page=1,
            per_page=10, order: str = 'ASC'
    ):
        """Method for sorting records by release_date and rating"""
        if order == 'ASC':
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 database.query(self.model).order_by(
                     self.model.release_date.asc(), self.model.rating.asc()
                 ).paginate(page=page, per_page=per_page).items])
        if order == 'DESC':
            return self.list_schema.from_orm(
                [self.schema.from_orm(item) for item in
                 database.query(self.model).order_by(
                     self.model.release_date.desc(), self.model.rating.desc()
                 ).paginate(page=page, per_page=per_page).items])

        return None


FILM = CRUDFilm(Film, FilmBase, FilmList)
