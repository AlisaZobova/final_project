"""Endpoints for genre"""

from flask_restx import Resource

from app.crud import GENRE
from app.endpoints.todo import API, TODO


@API.route('/genre/<int:genre_id>', endpoint='genre')
@API.route('/genre', methods=['POST'], endpoint='genre_create')
@API.doc(params={'genre_id': 'An ID'})
class Genre(Resource):
    """Class for implementing genre HTTP requests"""
    def get(self, genre_id):
        """Processing a get request"""
        return TODO.get(record_id=genre_id, crud=GENRE)

    def post(self):
        """Processing a post request"""
        return TODO.create(crud=GENRE)

    def put(self, genre_id):
        """Processing a put request"""
        return TODO.update(record_id=genre_id, crud=GENRE)

    def delete(self, genre_id):
        """Processing a delete request"""
        return TODO.delete(record_id=genre_id, crud=GENRE)


@API.route('/genres/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='genres_default')
@API.route('/genres/<int:page>/<int:per_page>', methods=['GET'], endpoint='genres')
class Genres(Resource):
    """Class for implementing genres get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        return TODO.read_all(crud=GENRE, page=page, per_page=per_page)