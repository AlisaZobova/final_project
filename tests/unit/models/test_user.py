from werkzeug.security import check_password_hash

from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(role_id=1, name='John', email='johny@gmail.com', password='John555')
    assert user.email == 'johny@gmail.com'
    assert check_password_hash(user.password, 'John555') is True
    assert user.role_id == 1
    assert user.name == 'John'
