"""Endpoints for genre"""

from flask_restx import Resource, fields

from app.crud import GENRE
from app.endpoints.todo import genre, TODO


genre_model = genre.model('Genre', {
    'genre_name': fields.String(description='Genre name', example='Comedy')
})


@genre.route('/<int:genre_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='genre')
@genre.route('', methods=['POST'], endpoint='genre_create')
class Genre(Resource):
    """Class for implementing genre HTTP requests"""
    @genre.doc(params={'genre_id': 'An ID'})
    def get(self, genre_id):
        """Get one record from the genre table"""
        return TODO.get(record_id=genre_id, crud=GENRE)

    @genre.doc(model=genre_model, body=genre_model)
    def post(self):
        """Create new record in the genre table"""
        return TODO.create(crud=GENRE)

    @genre.doc(params={'genre_id': 'An ID'})
    def put(self, genre_id):
        """Update a record in the genre table"""
        return TODO.update(record_id=genre_id, crud=GENRE)

    @genre.doc(params={'genre_id': 'An ID'})
    def delete(self, genre_id):
        """Delete a record from the genre table"""
        return TODO.delete(record_id=genre_id, crud=GENRE)


@genre.route('/all/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='genres_default')
@genre.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='genres')
@genre.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Genres(Resource):
    """Class for implementing genres get multy request"""
    def get(self, page, per_page):
        """Get all records from the genre table"""
        return TODO.read_all(crud=GENRE, page=page, per_page=per_page)
