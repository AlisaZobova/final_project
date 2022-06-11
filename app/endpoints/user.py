"""Endpoints for user"""

from flask_restx import Resource, fields
from sqlalchemy.exc import IntegrityError

from app.crud import USER
from app.endpoints.todo import TODO
from .namespaces import user


USER_MODEL = user.model(
    'User Create', {'role_id': fields.Integer(description='User role id', example=1),
             'name': fields.String(description='User name', example='John'),
             'email': fields.String(description='User email', example='john@gmail.com'),
             'password': fields.String(description='User password', example='Johny5863')
             })

MODEL = user.model(
    'User', {'name': fields.String(description='User name', example='John'),
             'email': fields.String(description='User email', example='john@gmail.com')})


@user.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='user')
@user.route('', methods=['POST'], endpoint='user_create')
class User(Resource):
    """Class for implementing user HTTP requests"""
    @user.response(404, 'Not Found')
    @user.doc(params={'user_id': 'An ID'})
    def get(self, user_id):
        """Get one record from the user table"""
        return TODO.get(record_id=user_id, crud=USER, t_name='user')

    @user.response(201, 'Created', MODEL)
    @user.response(400, 'Validation Error')
    @user.doc(body=USER_MODEL)
    def post(self):
        """Create new record in the user table"""
        try:
            return TODO.create(crud=USER, t_name='user')
        except IntegrityError:
            user.abort(400, "User with such email already exist.")

    @user.response(400, 'Validation Error')
    @user.response(404, 'Not Found')
    @user.doc(params={'user_id': 'An ID'}, body=USER_MODEL, model=MODEL)
    def put(self, user_id):
        """Update a record in the user table"""
        try:
            return TODO.update(record_id=user_id, crud=USER, t_name='user')
        except IntegrityError:
            user.abort(400, "User with such email already exist.")

    @user.response(204, 'Record deleted successfully')
    @user.response(404, 'Not Found')
    @user.doc(params={'user_id': 'An ID'})
    def delete(self, user_id):
        """Delete a record from the user table"""
        return TODO.delete(record_id=user_id, crud=USER, t_name='user')


@user.route('/all/<int:page>', methods=['GET'],
            defaults={'per_page': 10}, endpoint='users_default')
@user.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='users')
@user.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Users(Resource):
    """Class for implementing users get multy request"""
    @user.response(404, 'Not Found')
    def get(self, page, per_page):
        """Get all records from the user table"""
        return TODO.read_all(crud=USER, page=page, per_page=per_page, t_name='user')
