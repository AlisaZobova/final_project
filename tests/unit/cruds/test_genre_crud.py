"""Testing genre's delete method"""

from faker import Faker

from app import DATABASE
from app.crud import GENRE
from app.models import Film, Genre


def test_delete(app_with_data):
    """
    Verifying the deletion of a record from the genre's
    table along with relationships in the associated table
    """
    fake = Faker()
    count = len(DATABASE.session.query(Film).all())
    for i in range(1, 6):
        film_values = {
            'user_id': 4, 'title': f'Film {i}',
            'poster': fake.url(), 'description': fake.text(), 'release_date': "2000-01-01",
            'rating': round(fake.pyfloat(min_value=0, max_value=10), 1)
            }
        DATABASE.session.add(Film(**film_values))
        genre = DATABASE.session.query(Genre).get(5)
        film = DATABASE.session.query(Film).get(count+i)
        film.genres.append(genre)

    GENRE.remove(database=DATABASE.session, record_id=5)

    assert len(DATABASE.session.query(Film).all()) == count + 5

    for film in DATABASE.session.query(Film).filter(Film.film_id > count).all():
        assert film.genres == []
