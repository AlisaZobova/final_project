"""Module with base CRUD realisation"""

from typing import Any, Dict, Generic, List, Optional, Union
from fastapi.encoders import jsonable_encoder
from app.models.db_init import DATABASE
from .abstract import CRUDAbstract, ModelType, CreateSchemaType, \
                      UpdateSchemaType, BaseSchemaType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType], CRUDAbstract):
    """
    CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    **Parameters**
    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    * `list_schema`: A list of Pydantic models
    """

    def get(self, database: DATABASE.session, record_id: Any) -> Optional[BaseSchemaType]:
        """Method to read one record by id"""
        return self.schema.from_orm(database.query(self.model).get(record_id))

    def get_multi(
            self, database: DATABASE.session, *,
            page=1, per_page: int = 10
    ) -> List[BaseSchemaType]:
        """Method to read all records from a table with default pagination set to 10"""
        return self.list_schema.from_orm(
            [self.schema.from_orm(item) for item in database.query(self.model).paginate(
                page=page, per_page=per_page).items])

    def create(self, database: DATABASE.session, obj_in: Union[CreateSchemaType, Dict[str, Any]],
               **kwargs) -> BaseSchemaType:
        """Method to create one record"""
        obj_in_data = jsonable_encoder(obj_in)
        database_obj = self.model(**obj_in_data)
        database.add(database_obj)
        database.commit()
        database.refresh(database_obj)
        return self.schema.from_orm(database_obj)

    def update(self, database: DATABASE.session, *, database_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseSchemaType:
        """Method to update one record"""
        obj_data = jsonable_encoder(database_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(database_obj, field, update_data[field])
        database.add(database_obj)
        database.commit()
        database.refresh(database_obj)
        return self.schema.from_orm(database_obj)

    def remove(self, database: DATABASE.session, *, record_id: int) -> BaseSchemaType:
        """Method to delete one record by id"""
        obj = database.query(self.model).get(record_id)
        database.delete(obj)
        database.commit()
        return self.schema.from_orm(obj)
