"""Module with authentication"""

from flask_restx import Resource, fields
from flask import request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user

from app.models import User
from app.endpoints.todo import authentication as auth


auth_model = auth.model('Authentication', {
    'email': fields.String(description='User email', example='thomas@gmail.com'),
    'password': fields.String(description='User password', example='Shelby2013')
})


@auth.doc(model=auth_model, body=auth_model)
@auth.route('/login', methods=['POST'])
class Login(Resource):
    def post(self):
        """Login method"""
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return 'NO SUCH USER!'

        if not check_password_hash(user.password, password):
            flash('Please check your password and try again.')
            return 'WRONG PASSWORD!'

        login_user(user)
        return 'OK'


@login_required
@auth.route('/logout', methods=['GET'])
class Logout(Resource):
    def get(self):
        """Logout method"""
        logout_user()
        return 'SUCCESSFULLY LOGOUT'
