"""Module with abstract CRUD realisation"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class CRUDAbstract(ABC):
    """
    CRUD class with abstract methods to Create, Read, Update, Delete (CRUD).
    """

    @abstractmethod
    def get(self, record_id: Any):
        """Method to read one record by id"""

    @abstractmethod
    def get_multi(self, *, page: int = 1, per_page: int = 10):
        """Method to read all records from a table with default pagination set to 10"""

    @abstractmethod
    def create(self, obj_in: Dict[str, Any], **kwargs):
        """Method to create one record"""

    @abstractmethod
    def update(self, *, record_id: int, obj_in: Dict[str, Any]):
        """Method to update one record"""

    @abstractmethod
    def remove(self, *, record_id: int):
        """Method to delete one record by id"""
