"""Module with authentication"""

from flask import Blueprint, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user

from app.models import User

AUTH = Blueprint('auth', __name__)


@AUTH.route('/login', methods=['POST'])
def login_post():
    """Login method"""
    email = request.args.get('email')
    password = request.args.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return 'NO SUCH USER!'

    if not check_password_hash(user.password, password):
        flash('Please check your password and try again.')
        return 'WRONG PASSWORD!'

    login_user(user)
    return 'OK'


@AUTH.route('/logout')
@login_required
def logout():
    """Logout method"""
    logout_user()
    return 'SUCCESSFULLY LOGOUT'
