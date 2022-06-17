"""Module with abstract CRUD realisation"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Union, Type
from pydantic import BaseModel
from app.models.db_init import db

ModelType = TypeVar("ModelType", bound=db.Model)
BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseModel)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDAbstract(ABC):
    """
    CRUD class with abstract methods to Create, Read, Update, Delete (CRUD).
    """

    def __init__(self, model: Type[ModelType], schema: Type[BaseSchemaType],
                 update_schema: Type[UpdateSchemaType], list_schema: Type[ListSchemaType],
                 database=db.session):
        self.model = model
        self.schema = schema
        self.list_schema = list_schema
        self.update_schema = update_schema
        self.database = database

    @abstractmethod
    def get(self, record_id: Any) -> Optional[BaseSchemaType]:
        """Method to read one record by id"""

    @abstractmethod
    def get_multi(self, *, page=1, per_page: int = 10) -> List[BaseSchemaType]:
        """Method to read all records from a table with default pagination set to 10"""

    @abstractmethod
    def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]], **kwargs) -> BaseSchemaType:
        """Method to create one record"""

    @abstractmethod
    def update(self, *, record_id: int,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseSchemaType:
        """Method to update one record"""

    @abstractmethod
    def remove(self, *, record_id: int) -> ModelType:
        """Method to delete one record by id"""
