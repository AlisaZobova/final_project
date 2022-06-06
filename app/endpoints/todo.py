"""Module with class with basic methods for future endpoints"""

from flask import Blueprint, request, jsonify
from flask_restx import Api

from app.crud.abstract import CRUDAbstract
from app.domain import read, create, update, delete, read_multy

API_BP = Blueprint('api', __name__)

API = Api(API_BP)


class TodoBase:
    """Class with basic methods for future endpoints"""
    def get(self, record_id: int, crud: CRUDAbstract):
        """Method for future get request"""
        record = read(crud, record_id).dict()
        if record is not None:
            return record
        API.abort(404, "Record doesn't exist")

    def create(self, crud: CRUDAbstract):
        """Method for future post request"""
        data = request.args
        return create(crud, data).dict()

    def update(self, record_id: int, crud: CRUDAbstract):
        """Method for future put request"""
        data = request.args
        return update(crud, record_id, data).dict()

    def delete(self, crud: CRUDAbstract, record_id: int):
        """Method for future delete request"""
        return delete(crud, record_id).dict()

    def read_all(self, crud: CRUDAbstract, page: int, per_page: int):
        """Method for future get multy request"""
        records = read_multy(crud, page=page, per_page=per_page).dict()
        return jsonify(records['__root__'])


TODO = TodoBase()
