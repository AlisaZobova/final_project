"""Endpoints for user"""

from flask_restx import Resource, fields

from app.crud import user
from app.endpoints.todo import todo
from loggers import logger
from .namespaces import user_ns

user_create_update_model = user_ns.model(
    'User Create', {'role_id': fields.Integer(description='User role id', example=2),
                    'name': fields.String(description='User name', example='John'),
                    'email': fields.String(description='User email', example='john@gmail.com'),
                    'password': fields.String(description='User password', example='Johny5863')
                    })

user_model = user_ns.model(
    'User', {'name': fields.String(description='User name', example='John'),
             'email': fields.String(description='User email', example='john@gmail.com')})


@user_ns.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='user')
@user_ns.route('', methods=['POST'], endpoint='user_create')
class User(Resource):
    """Class for implementing user HTTP requests"""

    @user_ns.doc(
        model=user_model,
        params={'user_id': 'An ID'},
        responses={200: 'Success', 404: 'Not Found'}
    )
    def get(self, user_id):
        """Get one record from the user table"""
        return todo.get(record_id=user_id, crud=user, t_name='user')

    @user_ns.response(201, 'Record created successfully', user_model)
    @user_ns.response(400, 'Validation Error')
    @user_ns.doc(body=user_create_update_model)
    def post(self):
        """Create new record in the user table"""
        try:
            return todo.create(crud=user, t_name='user')
        except ValueError:
            logger.error("Attempt to create user with email that already exist.")
            user_ns.abort(400, "User with such email already exist.")

    @user_ns.doc(
        params={'user_id': 'An ID'},
        body=user_create_update_model,
        model=user_model,
        responses={200: 'Record updated successfully',
                   400: 'Validation Error',
                   404: 'Not Found'}
    )
    def put(self, user_id):
        """Update a record in the user table"""
        try:
            return todo.update(record_id=user_id, crud=user, t_name='user')
        except ValueError:
            logger.error("Attempt to update the email to the one that is already in the database.")
            user_ns.abort(400, "User with such email already exist.")

    @user_ns.doc(
        params={'user_id': 'An ID'},
        responses={204: 'Record deleted successfully',
                   404: 'Not Found'}
    )
    def delete(self, user_id):
        """Delete a record from the user table"""
        return todo.delete(record_id=user_id, crud=user, t_name='user')


@user_ns.route('/all/<int:page>', methods=['GET'],
               defaults={'per_page': 10}, endpoint='users_default')
@user_ns.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='users')
@user_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Users(Resource):
    """Class for implementing users get multy request"""

    @user_ns.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, page, per_page):
        """Get all records from the user table"""
        return todo.read_all(crud=user, page=page, per_page=per_page, t_name='user')
