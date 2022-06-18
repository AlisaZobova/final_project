"""Testing director's delete method"""

from faker import Faker

from app import db
from app.crud import director
from app.models import Film, Director


def test_delete(app_with_data):
    """
    Verifying the deletion of a record from the director's
    table along with relationships in the associated table
    """
    fake = Faker()
    count = len(db.session.query(Film).all())
    for i in range(1, 6):
        film_values = {
            'user_id': 4, 'title': f'Test Film {i}',
            'poster': fake.url(), 'description': fake.text(), 'release_date': "2000-01-01",
            'rating': round(fake.pyfloat(min_value=0, max_value=10), 1)
            }
        db.session.add(Film(**film_values))
        get_director = db.session.query(Director).get(5)
        film = db.session.query(Film).get(count + i)
        film.directors.append(get_director)

    director.remove(record_id=5)

    assert len(db.session.query(Film).all()) == count + 5

    for film in db.session.query(Film).filter(Film.film_id > count).all():
        assert film.directors == []
