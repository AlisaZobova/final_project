"""Endpoints for role"""

from flask_restx import Resource

from app.crud import ROLE
from app.endpoints.todo import api, TODO


@api.route('/role/<int:role_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='role')
@api.route('/role', methods=['POST'], endpoint='role_create')
@api.doc(params={'role_id': 'An ID'})
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


@api.route('/role/all/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='roles_default')
@api.route('/role/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='roles')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Roles(Resource):
    """Class for implementing roles get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        return TODO.read_all(crud=ROLE, page=page, per_page=per_page)
