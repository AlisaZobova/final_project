"""Module with class with basic methods for future endpoints"""
import flask
from flask import request, jsonify
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.exceptions import NotFound

from app.crud.abstract import CRUDAbstract
from app.domain import read, create, update, delete, read_multy
from loggers import logger
from .namespaces import api


class TodoBase:
    """Class with basic methods for future endpoints"""
    def get(self, record_id: int, crud: CRUDAbstract, t_name: str):
        """Method for future get request"""
        try:
            record = read(crud, record_id).dict()
            logger.info('Returned %s with ID %d.', t_name, record_id)
            return record
        except ValidationError:
            logger.error("Attempt to get record with id %d, that doesn't exist.", record_id)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")
            return None

    def create(self, crud: CRUDAbstract, t_name: str):
        """Method for future post request"""
        try:
            data = request.json
            record = create(crud, data).dict()
            logger.info('Created new %s with such fields:\n%s.', t_name, str(data))
            return record, 201
        except (ValidationError, DataError):
            logger.error("Incorrect data entered. "
                         "The record in %s table could not be created.", t_name)
            api.abort(400, "Incorrect data entered. The record could not be created.")
            return None

    def update(self, record_id: int, crud: CRUDAbstract, t_name: str):
        """Method for future put request"""
        try:
            data = request.json
            record = update(crud, record_id, data).dict()
            logger.info('Updated %s with id %d. New fields:\n%s.', t_name, record_id, str(data))
            return record
        except (ValidationError, DataError):
            logger.error("Incorrect data entered. "
                         "The record in %s table could not be updated.", t_name)
            api.abort(400, "Incorrect data entered. The record could not be updated.")
            return None
        except TypeError:
            logger.error('Attempt to update record with id %s in %s table, '
                         'but record does not exist.', record_id, t_name)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")
            return None

    def delete(self, crud: CRUDAbstract, record_id: int, t_name: str):
        """Method for future delete request"""
        try:
            record = delete(crud, record_id).dict()
            logger.info('Deleted %s with ID %d. %s', t_name, record_id, str(record))
            return flask.Response(status=204)
        except UnmappedInstanceError:
            logger.error("Attempt to delete record from %s table with id %d, "
                         "that doesn't exist.", t_name, record_id)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")
            return None

    def read_all(
            self, crud: CRUDAbstract, page: int, per_page: int, t_name: str
    ):
        """Method for future get multy request"""
        try:
            records = read_multy(crud, page=page, per_page=per_page).dict()

            logger.info('Returned the %d page of %s table records '
                        'paginated with %d records per page.',
                        page, t_name, per_page)
            return jsonify(records['__root__'])
        except NotFound:
            logger.warning("No more records in %s table.", t_name)
            api.abort(404, message=f"No more records in {t_name} table.")
            return None


todo = TodoBase()
