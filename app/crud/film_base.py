"""Module with abstract class for additional requests to the film model"""

from abc import ABC, abstractmethod
from typing import List

from app.schemas import FilmList


class FilmAbstract(ABC):
    """Abstract class for additional requests to the film model"""
    @abstractmethod
    def get_multi_by_title(
            self, title: str, page: int = 1, per_page: int = 10
    ) -> FilmList:
        """A method that searches for a partial match of a film title"""

    @abstractmethod
    def query_film_multy_filter(
            self, values: List[str], page: int = 1, per_page=10
    ) -> FilmList:
        """Method for filtering records by genres, release_date and directors"""

    @abstractmethod
    def query_film_multy_sort(
            self, order: List[str], page: int = 1, per_page: int = 10
    ) -> FilmList:
        """Method for sorting records by release_date and rating"""
