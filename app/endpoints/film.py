"""Endpoints for film"""
import json

from flask import request, jsonify
from flask_restx import Resource

from app.crud import FILM
from app.endpoints.todo import API, TODO
from app.domain import create_film, read_films, set_unknown_director_multy, \
    query_film_multy_sort, query_film_multy_filter, set_unknown_director, get_multi_by_title


@API.route('/film/<int:film_id>', endpoint='film')
@API.route('/film', methods=['POST'], endpoint='film_create')
@API.doc(params={'film_id': 'An ID'})
class Film(Resource):
    """Class for implementing film HTTP requests"""
    def get(self, film_id):
        """Processing a get request"""
        film = TODO.get(record_id=film_id, crud=FILM)
        return set_unknown_director(film)

    def post(self):
        """Processing a post request"""
        directors_id = request.args.get('directors')
        genres_id = request.args.get('genres')
        values = {
            'title': request.args.get('title'),
            'poster': request.args.get('poster'),
            'description': request.args.get('description', default='Film has no description.'),
            'release_date': request.args.get('release_date'),
            'rating': request.args.get('rating'),
            'user_id': request.args.get('user_id')
        }
        return create_film(FILM, values=values,
                                   directors_id=directors_id,
                                   genres_id=genres_id)

    def put(self, film_id):
        """Processing a put request"""
        film = TODO.update(record_id=film_id, crud=FILM)
        return set_unknown_director(film)

    def delete(self, film_id):
        """Processing a delete request"""
        film = TODO.delete(record_id=film_id, crud=FILM)
        return set_unknown_director(film)


@API.route('/films/<int:page>', methods=['GET'], defaults={'per_page': 10}, endpoint='films_default')
@API.route('/films/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_per_page')
class Films(Resource):
    """Class for implementing films get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        films = read_films(crud=FILM, page=page, per_page=per_page).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@API.route('/films/<string:title>/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_title_default')
@API.route('/films/<string:title>/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_title_per_page')
class FilmsTitle(Resource):
    """Class for implementing films get multy request"""
    def get(self, page, per_page, title):
        """Processing a get multy request"""
        films = get_multi_by_title(film_crud=FILM, page=page, per_page=per_page, title=title).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@API.route('/films/filter/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_filter_default')
@API.route('/films/filter/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_filter')
class FilmsFiltered(Resource):
    """Class for implementing films get multy filtered request"""
    def get(self, page, per_page):
        """Processing a get multy filtered request"""
        data = [request.args.get('release_date', default=None),
                request.args.get('directors', default=None),
                request.args.get('genres', default=None)]
        films = query_film_multy_filter(film_crud=FILM, values=data, page=page, per_page=per_page).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@API.route('/films/sort/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_sort_default')
@API.route('/films/sort/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_sort')
class FilmsSorted(Resource):
    """Class for implementing films get multy sorted request"""
    def get(self, page: int, per_page: int):
        """Processing a get multy sorted request"""
        order = [request.args.get('release_date', default=None),
                 request.args.get('rating', default=None)]
        films = query_film_multy_sort(film_crud=FILM, page=page, per_page=per_page, order=order).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])