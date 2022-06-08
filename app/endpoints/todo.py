"""Module with class with basic methods for future endpoints"""

from flask import Blueprint, request, jsonify
from flask_restx import Api

from app.crud.abstract import CRUDAbstract
from app.domain import read, create, update, delete, read_multy

api_bp = Blueprint('api', __name__)  # pylint: disable=C0103

api = Api(api_bp)  # pylint: disable=C0103

director = api.namespace('director', description='Director namespace')
api.add_namespace(director)

film = api.namespace('film', description='Film namespace')
api.add_namespace(film)

genre = api.namespace('genre', description='Genre namespace')
api.add_namespace(genre)

user = api.namespace('user', description='User namespace')
api.add_namespace(user)

authentication = api.namespace('authentication', description='Authentication namespace')
api.add_namespace(authentication, path='/auth')


class TodoBase:
    """Class with basic methods for future endpoints"""
    def get(self, record_id: int, crud: CRUDAbstract):
        """Method for future get request"""
        record = read(crud, record_id).dict()
        if record is not None:
            return record
        api.abort(404, "Record doesn't exist")

    def create(self, crud: CRUDAbstract):
        """Method for future post request"""
        data = request.json
        return create(crud, data).dict()

    def update(self, record_id: int, crud: CRUDAbstract):
        """Method for future put request"""
        data = request.json
        return update(crud, record_id, data).dict()

    def delete(self, crud: CRUDAbstract, record_id: int):
        """Method for future delete request"""
        return delete(crud, record_id).dict()

    def read_all(self, crud: CRUDAbstract, page: int, per_page: int):
        """Method for future get multy request"""
        if bool(request.args.get('per_page')):
            per_page = int(request.args.get('per_page'))
        records = read_multy(crud, page=page, per_page=per_page).dict()
        return jsonify(records['__root__'])


TODO = TodoBase()
