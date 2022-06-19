"""Endpoints for director"""

from flask_restx import Resource, fields

from app.crud import director
from app.endpoints.todo import todo
from .namespaces import director_ns

director_model = director_ns.model('Director', {
    'name': fields.String(description='Director name', example='Thomas'),
    'surname': fields.String(description='Director surname', example='Shelby')
})


@director_ns.route('/<int:director_id>', endpoint='director', methods=['GET', 'PUT', 'DELETE'])
@director_ns.route('', methods=['POST'], endpoint='director_create')
class Director(Resource):
    """Class for implementing director HTTP requests"""

    @director_ns.doc(
        model=director_model,
        params={'director_id': 'An ID'},
        responses={200: 'Success', 404: 'Not Found'}
    )
    def get(self, director_id):
        """Get one record from the director table"""
        return todo.get(record_id=director_id, crud=director, t_name='director')

    @director_ns.response(201, 'Record created successfully', director_model)
    @director_ns.response(400, 'Validation Error')
    @director_ns.doc(body=director_model)
    def post(self):
        """Create new record in the director table"""
        return todo.create(crud=director, t_name='director')

    @director_ns.doc(
        params={'director_id': 'An ID'},
        model=director_model,
        body=director_model,
        responses={200: 'Record updated successfully',
                   400: 'Validation Error',
                   404: 'Not Found'}
    )
    def put(self, director_id):
        """Update a record in the director table"""
        return todo.update(record_id=director_id, crud=director, t_name='director')

    @director_ns.doc(
        params={'director_id': 'An ID'},
        responses={204: 'Record deleted successfully',
                   404: 'Not Found'}
    )
    def delete(self, director_id):
        """Delete a record from the director table"""
        return todo.delete(record_id=director_id, crud=director, t_name='director')


@director_ns.route('/all/<int:page>', defaults={'per_page': 10},
                   methods=['GET'], endpoint='directors_default')
@director_ns.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='directors')
@director_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'},
                 responses={200: 'Success', 404: 'Not Found'})
class Directors(Resource):
    """Class for implementing directors get multy request"""
    @director_ns.doc(responses={200: 'Success', 404: 'Not Found'})
    def get(self, page, per_page):
        """Get all records from the director table"""
        return todo.read_all(crud=director, page=page, per_page=per_page, t_name='director')
