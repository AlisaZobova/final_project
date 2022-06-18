"""Module for test subfunctions"""


def check_count(response, code, count):
    """Function for checking response length"""
    assert response.status_code == code
    data = response.json

    if count != 0:
        assert len(data) == count
