"""Endpoints for director"""

from flask_restx import Resource

from app.crud import DIRECTOR
from app.endpoints.todo import api, TODO


@api.route('/director/<int:director_id>', endpoint='director', methods=['GET', 'PUT', 'DELETE'])
@api.route('/director', methods=['POST'], endpoint='director_create')
@api.doc(params={'director_id': 'An ID'})
class Director(Resource):
    """Class for implementing director HTTP requests"""
    def get(self, director_id):
        """Processing a get request"""
        return TODO.get(record_id=director_id, crud=DIRECTOR)

    def post(self):
        """Processing a post request"""
        return TODO.create(crud=DIRECTOR)

    def put(self, director_id):
        """Processing a put request"""
        return TODO.update(record_id=director_id, crud=DIRECTOR)

    def delete(self, director_id):
        """Processing a delete request"""
        return TODO.delete(record_id=director_id, crud=DIRECTOR)


@api.route('/director/all/<int:page>', defaults={'per_page': 10},
           methods=['GET'], endpoint='directors_default')
@api.route('/director/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='directors')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Directors(Resource):
    """Class for implementing directors get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        return TODO.read_all(crud=DIRECTOR, page=page, per_page=per_page)



