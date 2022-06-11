"""Endpoints for director"""

from flask_restx import Resource, fields

from app.crud import DIRECTOR
from app.endpoints.todo import TODO
from .namespaces import director


DIRECTOR_MODEL = director.model('Director', {
    'name': fields.String(description='Director name', example='Thomas'),
    'surname': fields.String(description='Director surname', example='Shelby')
})


@director.route('/<int:director_id>', endpoint='director', methods=['GET', 'PUT', 'DELETE'])
@director.route('', methods=['POST'], endpoint='director_create')
class Director(Resource):
    """Class for implementing director HTTP requests"""
    @director.doc(params={'director_id': 'An ID'})
    @director.response(404, 'Not Found')
    def get(self, director_id):
        """Get one record from the director table"""
        return TODO.get(record_id=director_id, crud=DIRECTOR, t_name='director')

    @director.response(201, 'Created', DIRECTOR_MODEL)
    @director.response(400, 'Validation Error')
    @director.doc(body=DIRECTOR_MODEL)
    def post(self):
        """Create new record in the director table"""
        return TODO.create(crud=DIRECTOR, t_name='director')

    @director.response(400, 'Validation Error')
    @director.response(404, 'Not Found')
    @director.doc(params={'director_id': 'An ID'}, model=DIRECTOR_MODEL, body=DIRECTOR_MODEL)
    def put(self, director_id):
        """Update a record in the director table"""
        return TODO.update(record_id=director_id, crud=DIRECTOR, t_name='director')

    @director.response(204, 'Record deleted successfully')
    @director.response(404, 'Not Found')
    @director.doc(params={'director_id': 'An ID'})
    def delete(self, director_id):
        """Delete a record from the director table"""
        return TODO.delete(record_id=director_id, crud=DIRECTOR, t_name='director')


@director.route('/all/<int:page>', defaults={'per_page': 10},
                methods=['GET'], endpoint='directors_default')
@director.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='directors')
@director.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Directors(Resource):
    """Class for implementing directors get multy request"""
    @director.response(404, 'Not Found')
    def get(self, page, per_page):
        """Get all records from the director table"""
        return TODO.read_all(crud=DIRECTOR, page=page, per_page=per_page, t_name='director')
