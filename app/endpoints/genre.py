"""Endpoints for genre"""

from flask_restx import Resource, fields
from app.crud import genre
from app.endpoints.todo import todo
from loggers import logger
from .namespaces import genre_ns


genre_model = genre_ns.model('Genre', {
    'genre_name': fields.String(description='Genre name', example='Comedy')
})


@genre_ns.route('/<int:genre_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='genre')
@genre_ns.route('', methods=['POST'], endpoint='genre_create')
class Genre(Resource):
    """Class for implementing genre HTTP requests"""
    @genre_ns.doc(params={'genre_id': 'An ID'})
    @genre_ns.response(200, 'Success')
    @genre_ns.response(404, 'Not Found')
    def get(self, genre_id):
        """Get one record from the genre table"""
        return todo.get(record_id=genre_id, crud=genre, t_name='genre')

    @genre_ns.response(201, 'Created', genre_model)
    @genre_ns.response(400, 'Validation Error')
    @genre_ns.doc(body=genre_model)
    def post(self):
        """Create new record in the genre table"""
        try:
            return todo.create(crud=genre, t_name='genre')
        except ValueError:
            logger.error("Attempt to create genre with name that already exist.")
            genre_ns.abort(400, "Genre with such name already exist.")

    @genre_ns.response(200, 'Successfully update')
    @genre_ns.response(400, 'Validation Error')
    @genre_ns.response(404, 'Not Found')
    @genre_ns.doc(params={'genre_id': 'An ID'}, body=genre_model, model=genre_model)
    def put(self, genre_id):
        """Update a record in the genre table"""
        try:
            return todo.update(record_id=genre_id, crud=genre, t_name='genre')
        except ValueError:
            logger.error("Attempt to update the genre name to the one "
                         "that is already in the database.")
            genre_ns.abort(400, "Genre with such name already exist.")

    @genre_ns.response(204, 'Record deleted successfully')
    @genre_ns.response(404, 'Not Found')
    @genre_ns.doc(params={'genre_id': 'An ID'})
    def delete(self, genre_id):
        """Delete a record from the genre table"""
        return todo.delete(record_id=genre_id, crud=genre, t_name='genre')


@genre_ns.route('/all/<int:page>', methods=['GET'],
                defaults={'per_page': 10}, endpoint='genres_default')
@genre_ns.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='genres')
@genre_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Genres(Resource):
    """Class for implementing genres get multy request"""
    @genre_ns.response(200, 'Success')
    @genre_ns.response(404, 'Not Found')
    def get(self, page, per_page):
        """Get all records from the genre table"""
        return todo.read_all(crud=genre, page=page, per_page=per_page, t_name='genre')
