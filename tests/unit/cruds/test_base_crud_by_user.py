"""Base crud tests by user"""

import pytest

from app import db, User
from app.crud import user
from app.schemas import UserBase


@pytest.mark.parametrize("data, expected_type", [
    ({
        "role_id": 1,
        "name": "Jack",
        "email": "jack5863@gmail.com",
        "password": "Jack895"
    },
     UserBase)
])
def test_create(app_with_data, data, expected_type):
    """Checking the function of creating a record"""
    before = len(db.session.query(User).all())
    new_user = user.create(obj_in=data)
    after = len(db.session.query(User).all())
    assert isinstance(new_user, expected_type)
    assert after == before + 1


def test_create_error(app_with_data):
    """Checking that an entry with a duplicate email cannot be created and an error occurs"""
    with pytest.raises(ValueError):
        data = {
            "role_id": 1,
            "name": "Jack",
            "email": "jacky@gmail.com",
            "password": "Jack895"
        }
        user.create(obj_in=data)


def test_get(app_with_data):
    """Checking the returned data of the get method"""
    get_user = user.get(record_id=6)
    assert isinstance(get_user, UserBase)
    assert UserBase.from_orm(db.session.query(User).get(6)) == get_user


def test_get_multy(app_with_data):
    """Checking the returned data and the number of records of the get multy method"""
    users = user.get_multi()
    assert all(isinstance(user, UserBase) for user in users.__root__)
    assert len(users.dict()['__root__']) == 10


def test_update(app_with_data):
    """Checking the correctness of data update and return value"""
    user_before = db.session.query(User).get(6)
    state = db.inspect(user_before)
    upd_user = user.update(record_id=6, obj_in={
        "name": "Jack",
        "email": "jack350@gmail.com",
    })
    assert bool(state.attrs.name.history.unchanged)
    assert bool(state.attrs.email.history.unchanged)
    assert isinstance(upd_user, UserBase)
    assert upd_user.dict() == {
        "name": "Jack",
        "email": "jack350@gmail.com",
    }


def test_update_error(app_with_data):
    """Checking that an entry cannot be created  with a duplicate email and an error occurs"""
    with pytest.raises(ValueError):
        user.update(record_id=10, obj_in={
            "name": "Jack",
            "email": "jacky@gmail.com",
        })


def test_delete(app_with_data):
    """
    Record deletion check and comparison of the
    number of records before and after applying the function
    """
    before = len(db.session.query(User).all())
    del_user = user.remove(record_id=5)
    after = len(db.session.query(User).all())
    assert db.session.query(User).get(5) is None
    assert isinstance(del_user, UserBase)
    assert after == before - 1
