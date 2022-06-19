"""Module with the logical part of the project"""

from typing import Union, Dict, Any, List

from .crud.abstract import CRUDAbstract
from .crud.base import CreateSchemaType, UpdateSchemaType
from .crud.film_base import FilmAbstract


def read(crud: CRUDAbstract, record_id: int):
    """Method to read one record by id"""
    return crud.get(record_id=record_id)


def read_multy(crud: CRUDAbstract, page: int = 1, per_page: int = 10):
    """Method to read all records from a table with default pagination set to 10"""
    return crud.get_multi(page=page, per_page=per_page)


def create(crud: CRUDAbstract, values: Union[CreateSchemaType, Dict[str, Any]]):
    """Method to create one record"""
    return crud.create(obj_in=values)


def update(crud: CRUDAbstract, record_id: int, values: Union[UpdateSchemaType, Dict[str, Any]]):
    """Method to update one record"""
    return crud.update(record_id=record_id, obj_in=values)


def delete(crud: CRUDAbstract, record_id: int):
    """Method to delete one record by id"""
    return crud.remove(record_id=record_id)


def set_unknown_director(film: Dict[str, Any]) -> Dict[str, Any]:
    """Set directors = UNKNOWN if film has no any director"""
    if not bool(film['directors']):
        film['directors'] = 'UNKNOWN'
    film['release_date'] = film['release_date'].isoformat()
    return film


def create_film(
        crud: CRUDAbstract, values: Union[CreateSchemaType, Dict[str, Any]],
        directors_id: str, genres_id: str
):
    """Method to create one film record"""
    genres_id = genres_id.split('&')
    directors_id = directors_id.split('&')
    film = crud.create(obj_in=values, directors=directors_id, genres=genres_id)
    return film


def set_unknown_director_multy(films: Dict[str, List]) -> Dict[str, List]:
    """Set directors = UNKNOWN if film has no any director"""
    for film in films['__root__']:
        if not bool(film['directors']):
            film['directors'] = 'UNKNOWN'
        film['release_date'] = film['release_date'].isoformat()

    return films


def read_films(crud: CRUDAbstract, page: int = 1, per_page: int = 10):
    """Method to read all records from a table with default pagination set to 10"""
    return crud.get_multi(page=page, per_page=per_page)


def get_multi_by_title(film_crud: FilmAbstract, title: str, page: int = 1, per_page: int = 10):
    """A method that searches for a partial match of a movie title"""
    return film_crud.get_multi_by_title(page=page, per_page=per_page, title=title)


def query_film_multy_filter(
        film_crud: FilmAbstract, values: List[Union[str, None]],
        page: int = 1, per_page: int = 10
):
    """Method for filtering records by genres, release_date and directors"""
    return film_crud.query_film_multy_filter(page=page, per_page=per_page, values=values)


def query_film_multy_sort(
        film_crud: FilmAbstract, order: List[Union[str, None]],
        page: int = 1, per_page: int = 10
):
    """Method for sorting records by release_date and rating"""
    return film_crud.query_film_multy_sort(page=page, per_page=per_page, order=order)
