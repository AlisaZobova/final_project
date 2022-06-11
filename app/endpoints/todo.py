"""Module with class with basic methods for future endpoints"""

from flask import request, jsonify
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.crud.abstract import CRUDAbstract
from app.domain import read, create, update, delete, read_multy
from .namespaces import api


class TodoBase:
    """Class with basic methods for future endpoints"""
    def get(self, record_id: int, crud: CRUDAbstract, ns: api.namespace, t_name: str):
        """Method for future get request"""
        try:
            record = read(crud, record_id).dict()
            ns.logger.info('Returned %s with ID %d.', t_name, record_id)
            return record
        except ValidationError:
            ns.logger.error("Attempt to get record with id %d, that doesn't exist.", record_id)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")

    def create(self, crud: CRUDAbstract, ns: api.namespace, t_name: str):
        """Method for future post request"""
        try:
            data = request.json
            ns.logger.info('Created new %s with such fields:\n%s.', t_name, str(data))
            return create(crud, data).dict()
        except (ValidationError, DataError):
            ns.logger.error("Incorrect data entered. "
                            "The record in %s table could not be created.", t_name)
            return "Incorrect data entered. The record could not be created."
        except IntegrityError as error:
            ns.logger.error("Not all required fields have been completed. "
                            "Can't create a record in % table. %s", t_name, error)
            return "Not all required fields have been completed. Can't create a record."

    def update(self, record_id: int, crud: CRUDAbstract, ns: api.namespace, t_name: str):
        """Method for future put request"""
        try:
            data = request.json
            ns.logger.info('Updated %s with id %d. New fields:\n%s.', t_name, record_id, str(data))
            return update(crud, record_id, data).dict()
        except (ValidationError, DataError):
            ns.logger.error("Incorrect data entered. "
                            "The record in %s table could not be updated.", t_name)
            return "Incorrect data entered. The record could not be updated."
        except TypeError:
            ns.logger.error('Attempt to update record with id % in %s table, '
                            'but record does not exist.', record_id, t_name)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")

    def delete(self, crud: CRUDAbstract, record_id: int, ns: api.namespace, t_name: str):
        """Method for future delete request"""
        try:
            ns.logger.info(f'Deleted %s with ID %d.', t_name, record_id)
            return delete(crud, record_id).dict()
        except UnmappedInstanceError:
            ns.logger.error("Attempt to delete record with id %d, that doesn't exist.", record_id)
            api.abort(404, message=f"Record with id {record_id} doesn't exist.")

    def read_all(
            self, crud: CRUDAbstract, page: int, per_page: int,
            namespace: api.namespace, t_name: str
    ):
        """Method for future get multy request"""
        if bool(request.args.get('per_page')):
            per_page = int(request.args.get('per_page'))
        records = read_multy(crud, page=page, per_page=per_page).dict()
        namespace.logger.info('Returned the %d page of %s table records '
                              'paginated with %d records per page.',
                              page, t_name, per_page)
        return jsonify(records['__root__'])


TODO = TodoBase()
