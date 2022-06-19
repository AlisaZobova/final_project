"""Module with base CRUD realisation"""

from typing import Any, Dict, Generic, List, Optional, Union, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.models.db_init import db
from .abstract import CRUDAbstract


ModelType = TypeVar("ModelType", bound=db.Model)
BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseModel)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType], CRUDAbstract):
    """
    CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    **Parameters**
    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    * `update_schema`: A Pydantic update model (schema) class
    * `list_schema`: A list of Pydantic models
    * `database`: SQLAlchemy session
    """
    def __init__(self, model: Type[ModelType], schema: Type[BaseSchemaType],
                 update_schema: Type[UpdateSchemaType], list_schema: Type[ListSchemaType],
                 database=db.session):
        self.model = model
        self.schema = schema
        self.list_schema = list_schema
        self.update_schema = update_schema
        self.database = database

    def get(self, record_id: Any) -> Optional[BaseSchemaType]:
        """Method to read one record by id"""
        return self.schema.from_orm(self.database.query(self.model).get(record_id))

    def get_multi(
            self, *,
            page=1, per_page: int = 10
    ) -> List[BaseSchemaType]:
        """Method to read all records from a table with default pagination set to 10"""
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in self.database.query(self.model).paginate(
                page=page, per_page=per_page).items])

    def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]], **kwargs) -> BaseSchemaType:
        """Method to create one record"""
        record = self.check_validate_create(obj_in)
        database_obj = self.model(**obj_in)
        self.database.add(database_obj)
        self.database.commit()
        self.database.refresh(database_obj)
        return record

    def update(self, *, record_id: int,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseSchemaType:
        """Method to update one record"""
        database_obj = self.check_validate_update(obj_in, record_id)
        record = self.schema.from_orm(database_obj)
        self.database.commit()
        self.database.refresh(database_obj)
        return record

    def remove(self, *, record_id: int) -> ModelType:
        """Method to delete one record by id"""
        obj = self.database.query(self.model).get(record_id)
        self.database.delete(obj)
        self.database.commit()
        return self.schema.from_orm(obj)

    def check_db_error(self, data: Dict[str, Any]):
        """Method for checking database errors"""

    def check_validate_update(
            self, obj_in: Union[CreateSchemaType, Dict[str, Any]], record_id: int
    ):
        """Method returning a validated object to update"""
        database_obj = self.database.query(self.model).get(record_id)
        obj_data = jsonable_encoder(database_obj)
        self.check_db_error(obj_in)
        self.update_schema.parse_obj(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(database_obj, field, update_data[field])
        return database_obj

    def check_validate_create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]], **kwargs):
        """Method returning a validated object to create"""
        obj_in_data = jsonable_encoder(obj_in)
        self.check_db_error(obj_in_data)
        record = self.schema.parse_obj(obj_in_data)
        return record
