"""Endpoints for user"""

from flask_restx import Resource

from app.crud import USER
from app.endpoints.todo import api, TODO


@api.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='user')
@api.route('/user', methods=['POST'], endpoint='user_create')
@api.doc(params={'user_id': 'An ID'})
class User(Resource):
    """Class for implementing user HTTP requests"""
    def get(self, user_id):
        """Processing a get request"""
        return TODO.get(record_id=user_id, crud=USER)

    def post(self):
        """Processing a post request"""
        return TODO.create(crud=USER)

    def put(self, user_id):
        """Processing a put request"""
        return TODO.update(record_id=user_id, crud=USER)

    def delete(self, user_id):
        """Processing a delete request"""
        return TODO.delete(record_id=user_id, crud=USER)


@api.route('/user/all/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='users_default')
@api.route('/user/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='users')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Users(Resource):
    """Class for implementing users get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        return TODO.read_all(crud=USER, page=page, per_page=per_page)
