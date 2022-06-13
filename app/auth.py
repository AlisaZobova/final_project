"""Module with authentication"""

from flask import request, flash
from werkzeug.security import check_password_hash
from flask_restx import Resource, fields
from flask_login import login_user, login_required, logout_user, current_user

from app.models import User
from app.endpoints.namespaces import authentication as auth


AUTH_MODEL = auth.model('Authentication', {
    'email': fields.String(description='User email', example='john@gmail.com'),
    'password': fields.String(description='User password', example='Johny5863')
})


@auth.doc(model=AUTH_MODEL, body=AUTH_MODEL)
@auth.route('/login', methods=['POST'])
class Login(Resource):
    """Class for authentication"""
    @auth.response(400, 'Validation Error')
    @auth.response(404, 'Not Found')
    def post(self):
        """Login method"""
        try:
            email = request.json.get('email')
            password = request.json.get('password')

            if request.json == {}:
                raise AttributeError

            user = User.query.filter_by(email=email).first()

            if not user:
                auth.logger.warning('User with email %s does not exist.', email)
                auth.abort(404, 'NO SUCH USER!')

            if not check_password_hash(user.password, password):
                flash('Please check your password and try again.')
                auth.logger.warning('Wrong password entered.')
                auth.abort(400, 'WRONG PASSWORD!')

            login_user(user)
            auth.logger.info('%s successfully login.', current_user.name)
            return 'OK', 200

        except AttributeError:
            auth.logger.error(f'Not all authentication information received.')
            auth.abort(400, "Please enter your email and password.")


@login_required
@auth.route('/logout', methods=['GET'])
class Logout(Resource):
    """Class with method rof user logout"""
    @auth.response(200, 'Success')
    @auth.response(401, 'Unauthorized')
    def get(self):
        """Logout method"""
        try:
            user = current_user.name
            logout_user()
            auth.logger.info('%s successfully logout.', user)
            return 'SUCCESSFULLY LOGOUT', 200

        except AttributeError:
            auth.logger.error(f'No authorized users found. Logout impossible.')
            auth.abort(401, "No authorized users found!")
