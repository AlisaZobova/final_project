"""Module with the logical part of the project"""

from typing import Union, Dict, Any, List

from app import DATABASE
from app.models import Director, Genre
from .crud.abstract import CRUDAbstract, CreateSchemaType, UpdateSchemaType
from .crud.film_base import FilmAbstract


def read(crud: CRUDAbstract, record_id: int):
    """Method to read one record by id"""
    return crud.get(database=DATABASE.session, record_id=record_id)


def read_multy(crud: CRUDAbstract, page: int = 1, per_page: int = 10):
    """Method to read all records from a table with default pagination set to 10"""
    return crud.get_multi(page=page, per_page=per_page, database=DATABASE.session)


def create(crud: CRUDAbstract, values: Union[CreateSchemaType, Dict[str, Any]]):
    """Method to create one record"""
    return crud.create(database=DATABASE.session, obj_in=values)


def update(crud: CRUDAbstract, record_id: int, values: Union[UpdateSchemaType, Dict[str, Any]]):
    """Method to update one record"""
    obj = DATABASE.session.query(crud.model).get(record_id)
    return crud.update(database=DATABASE.session(), database_obj=obj, obj_in=values)


def delete(crud: CRUDAbstract, record_id: int):
    """Method to delete one record by id"""
    return crud.remove(database=DATABASE.session(), record_id=record_id)


def read_film(crud: CRUDAbstract, record_id: int):
    """Method to read one film record by id"""
    film = crud.get(database=DATABASE.session, record_id=record_id).dict()
    if not bool(film['directors']):
        film['directors'] = 'UNKNOWN'
    return film


def create_film(
        crud: CRUDAbstract, values: Union[CreateSchemaType, Dict[str, Any]],
        directors_id: str, genres_id: str
):
    """Method to create one film record"""
    genres_id = genres_id.split('&')
    directors_id = directors_id.split('&')
    directors = [DATABASE.session.query(Director).get(i) for i in directors_id]
    genres = [DATABASE.session.query(Genre).get(i) for i in genres_id]
    return crud.create(database=DATABASE.session, obj_in=values, directors=directors, genres=genres)


def set_unknown_director(films: Dict):
    """Set directors = UNKNOWN if film has no any director"""
    for film in films['__root__']:
        if not bool(film['directors']):
            film['directors'] = 'UNKNOWN'

    return films


def read_films(crud: CRUDAbstract, page: int = 1, per_page: int = 10):
    """Method to read all records from a table with default pagination set to 10"""
    films = crud.get_multi(page=page, per_page=per_page, database=DATABASE.session).dict()
    return set_unknown_director(films)


def get_multi_by_title(film_crud: FilmAbstract, title: str, page: int = 1, per_page: int = 10):
    """A method that searches for a partial match of a movie title"""
    films = film_crud.get_multi_by_title(page=page, per_page=per_page,
                                         database=DATABASE.session, title=title).dict()
    return set_unknown_director(films)


def query_film_filter(
        film_crud: FilmAbstract, column_name: str, value: str,
        page: int = 1, per_page: int = 10
):
    """Method for filtering records by release_date or genres or directors"""
    films = film_crud.query_film_filter(database=DATABASE.session, column_name=column_name,
                                        value=value, page=page, per_page=per_page).dict()
    return set_unknown_director(films)


def query_film_sort(
        film_crud: FilmAbstract, column_name: str, page: int = 1,
        per_page: int = 10, order: str = 'asc'
):
    """Method for sorting records by release_date or rating"""
    films = film_crud.query_film_sort(database=DATABASE.session, page=page, per_page=per_page,
                                      column_name=column_name, order=order).dict()
    return set_unknown_director(films)


def query_film_multy_filter(
        film_crud: FilmAbstract, values: List[str],
        page: int = 1, per_page: int = 10
):
    """Method for filtering records by genres, release_date and directors"""
    films = film_crud.query_film_multy_filter(database=DATABASE.session, page=page,
                                              per_page=per_page, values=values).dict()
    return set_unknown_director(films)


def query_film_multy_sort(
        film_crud: FilmAbstract, page: int = 1,
        per_page: int = 10, order: str = 'asc'
):
    """Method for sorting records by release_date and rating"""
    films = film_crud.query_film_multy_sort(database=DATABASE.session, page=page,
                                            per_page=per_page, order=order).dict()
    return set_unknown_director(films)
