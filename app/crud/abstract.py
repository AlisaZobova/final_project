"""Module with abstract CRUD realisation"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Union
from pydantic import BaseModel
from app.models.db_init import DATABASE

ModelType = TypeVar("ModelType", bound=DATABASE.Model)
BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseModel)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDAbstract(ABC):
    """
    CRUD class with abstract methods to Create, Read, Update, Delete (CRUD).
    """
    @abstractmethod
    def get(self, database: DATABASE.session, record_id: Any) -> Optional[BaseSchemaType]:
        """Method to read one record by id"""

    @abstractmethod
    def get_multi(
            self, database: DATABASE.session, *,
            page=1, per_page: int = 10
    ) -> List[BaseSchemaType]:
        """Method to read all records from a table with default pagination set to 10"""

    @abstractmethod
    def create(self, database: DATABASE.session, obj_in: Union[CreateSchemaType, Dict[str, Any]],
               **kwargs) -> BaseSchemaType:
        """Method to create one record"""

    @abstractmethod
    def update(self, database: DATABASE.session, *, database_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseSchemaType:
        """Method to update one record"""

    @abstractmethod
    def remove(self, database: DATABASE.session, *, record_id: int) -> ModelType:
        """Method to delete one record by id"""
