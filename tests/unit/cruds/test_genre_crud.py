"""Testing genre's delete method"""

from faker import Faker

from app import db
from app.crud import genre
from app.models import Film, Genre


def test_delete(app_with_data):
    """
    Verifying the deletion of a record from the genre's
    table along with relationships in the associated table
    """
    fake = Faker()
    count = len(db.session.query(Film).all())
    for i in range(1, 6):
        film_values = {
            'user_id': 4, 'title': f'Film {i}',
            'poster': fake.url(), 'description': fake.text(), 'release_date': "2000-01-01",
            'rating': round(fake.pyfloat(min_value=0, max_value=10), 1)
            }
        db.session.add(Film(**film_values))
        get_genre = db.session.query(Genre).get(5)
        film = db.session.query(Film).get(count + i)
        film.genres.append(get_genre)

    genre.remove(record_id=5)

    assert len(db.session.query(Film).all()) == count + 5

    for film in db.session.query(Film).filter(Film.film_id > count).all():
        assert film.genres == []
