"""Endpoints for role"""

from flask_restx import Resource

from app.crud import ROLE
from app.endpoints.todo import API, TODO


@API.route('/role/<int:role_id>', methods=['POST', 'PUT', 'GET'], endpoint='role')
@API.route('/role', methods=['POST'], endpoint='role_create')
@API.doc(params={'role_id': 'An ID'})
class Role(Resource):
    """Class for implementing role HTTP requests"""
    def get(self, role_id):
        """Processing a get request"""
        return TODO.get(record_id=role_id, crud=ROLE)

    def post(self):
        """Processing a post request"""
        return TODO.create(crud=ROLE)

    def put(self, role_id):
        """Processing a put request"""
        return TODO.update(record_id=role_id, crud=ROLE)


@API.route('/roles/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='roles_default')
@API.route('/roles/<int:page>/<int:per_page>', methods=['GET'], endpoint='roles')
class Roles(Resource):
    """Class for implementing roles get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        return TODO.read_all(crud=ROLE, page=page, per_page=per_page)
