"""Endpoints for film"""

from flask import request, jsonify, current_app
from flask_login import current_user
from flask_restx import Resource

from app.crud import FILM
from app.endpoints.todo import api, TODO
from app.domain import create_film, read_films, set_unknown_director_multy, \
    query_film_multy_sort, query_film_multy_filter, set_unknown_director, get_multi_by_title
from app.models import Film, Role


@api.route('/film/<int:film_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='film')
@api.route('/film', methods=['POST'], endpoint='film_create')
@api.doc(params={'film_id': 'An ID'})
class FilmBase(Resource):
    """Class for implementing film HTTP requests"""
    def get(self, film_id):
        """Processing a get request"""
        film = TODO.get(record_id=film_id, crud=FILM)
        return set_unknown_director(film)

    def post(self):
        """Processing a post request"""
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        directors_id = request.args.get('directors')
        genres_id = request.args.get('genres')
        values = {
            'title': request.args.get('title'),
            'poster': request.args.get('poster'),
            'description': request.args.get('description', default='Film has no description.'),
            'release_date': request.args.get('release_date'),
            'rating': request.args.get('rating'),
            'user_id': current_user.user_id
        }
        return create_film(FILM, values=values,
                                   directors_id=directors_id,
                                   genres_id=genres_id)

    def del_put_access(self, film_id):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        db_film = Film.query.get(film_id)
        admin = Role.query.filter_by(name='admin').first()
        if db_film.user_id != current_user.user_id and current_user.role_id != admin.role_id:
            return "Only the user who added the film or an administrator " \
                   "can make changes to a film. Access denied."
        return True

    def put(self, film_id):
        """Processing a put request"""
        access = self.del_put_access(film_id=film_id)
        if access is True:
            film = TODO.update(record_id=film_id, crud=FILM)
            return set_unknown_director(film)
        return access

    def delete(self, film_id):
        """Processing a delete request"""
        access = self.del_put_access(film_id=film_id)
        if access is True:
            film = TODO.delete(record_id=film_id, crud=FILM)
            return set_unknown_director(film)
        return access


@api.route('/film/all/<int:page>', methods=['GET'], defaults={'per_page': 10}, endpoint='films_default')
@api.route('/film/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_per_page')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Films(Resource):
    """Class for implementing films get multy request"""
    def get(self, page, per_page):
        """Processing a get multy request"""
        films = read_films(crud=FILM, page=page, per_page=per_page).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@api.route('/film/<string:title>/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_title_default')
@api.route('/film/<string:title>/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_title_per_page')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page', 'title': "Part of the film's title"})
class FilmsTitle(Resource):
    """Class for implementing films get multy request"""
    def get(self, page, per_page, title):
        """Processing a get multy request"""
        films = get_multi_by_title(film_crud=FILM, page=page, per_page=per_page, title=title).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@api.route('/film/filter/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_filter_default')
@api.route('/film/filter/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_filter')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class FilmsFiltered(Resource):
    """Class for implementing films get multy filtered request"""
    def get(self, page, per_page):
        """Processing a get multy filtered request"""
        data = [request.args.get('release_date', default=None),
                request.args.get('directors', default=None),
                request.args.get('genres', default=None)]
        films = query_film_multy_filter(film_crud=FILM, values=data, page=page, per_page=per_page).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])


@api.route('/film/sort/<int:page>', methods=['GET'],
           defaults={'per_page': 10}, endpoint='films_sort_default')
@api.route('/film/sort/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_sort')
@api.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class FilmsSorted(Resource):
    """Class for implementing films get multy sorted request"""
    def get(self, page: int, per_page: int):
        """Processing a get multy sorted request"""
        order = [request.args.get('release_date', default=None),
                 request.args.get('rating', default=None)]
        films = query_film_multy_sort(film_crud=FILM, page=page, per_page=per_page, order=order).dict()
        return jsonify(set_unknown_director_multy(films)['__root__'])
