"""Endpoints for user"""

from flask_restx import Resource, fields

from app.crud import USER
from app.endpoints.todo import user, TODO


user_model = user.model('User', {'role_id': fields.Integer(description='User role id', example=1),
                                 'name': fields.String(description='User name', example='John'),
                                 'email': fields.String(description='User email', example='john@gmail.com'),
                                 'password': fields.String(description='User password', example='Johny5863')
                                 })


@user.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='user')
@user.route('', methods=['POST'], endpoint='user_create')
class User(Resource):
    """Class for implementing user HTTP requests"""
    @user.doc(params={'user_id': 'An ID'})
    def get(self, user_id):
        """Get one record from the user table"""
        return TODO.get(record_id=user_id, crud=USER)

    @user.doc(model=user_model, body=user_model)
    def post(self):
        """Create new record in the user table"""
        return TODO.create(crud=USER)

    @user.doc(params={'user_id': 'An ID'})
    def put(self, user_id):
        """Update a record in the user table"""
        return TODO.update(record_id=user_id, crud=USER)

    @user.doc(params={'user_id': 'An ID'})
    def delete(self, user_id):
        """Delete a record from the user table"""
        return TODO.delete(record_id=user_id, crud=USER)


@user.route('/all/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='users_default')
@user.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='users')
@user.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Users(Resource):
    """Class for implementing users get multy request"""
    def get(self, page, per_page):
        """Get all records from the user table"""
        return TODO.read_all(crud=USER, page=page, per_page=per_page)
