"""Endpoints for film"""

from flask import request, jsonify
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import DataError
from werkzeug.exceptions import NotFound
from flask_login import current_user
from flask_restx import Resource, fields

from app.crud import film
from app.endpoints.todo import todo
from app.domain import create_film, read_films, set_unknown_director_multy, \
    query_film_multy_sort, query_film_multy_filter, set_unknown_director, get_multi_by_title
from app.models import Film, Role
from loggers import logger
from .namespaces import film_ns

film_create_model = film_ns.model('Film Create', {
    'title': fields.String(description='Film title', example='Peaky Blinders'),
    'poster': fields.String(description='Link to the poster',
                            example='https://www.posters.net/Peaky-Blinders-poster'),
    'description': fields.String(
        description='Film description',
        example='A gangster family epic set in 1900s England, centering on a gang who '
                'sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby.'
    ),
    'release_date': fields.Date(description='Film release date', example='2013-09-12'),
    'rating': fields.Float(description='Film rating', example='9.5'),
    'genres': fields.String(description='Film genres', example='1&2&4'),
    'directors': fields.String(description='Film directors', example='5&45')
})

film_update_model = film_ns.model('Film Update', {
    'title': fields.String(description='Film title', example='Peaky Blinders'),
    'poster': fields.String(description='Link to the poster',
                            example='https://www.posters.net/Peaky-Blinders-poster'),
    'description': fields.String(
        description='Film description',
        example='A gangster family epic set in 1900s England, centering on a gang who '
                'sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby.'
    ),
    'release_date': fields.Date(description='Film release date', example='2013-09-12'),
    'rating': fields.Float(description='Film rating', example='9.5')
})

film_model = film_ns.model('Film', {
    'title': fields.String(example='Peaky Blinders'),
    'poster': fields.String(example='https://www.posters.net/Peaky-Blinders-poster'),
    'description': fields.String(
        example='A gangster family epic set in 1900s England, centering on a gang who '
                'sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby.'
    ),
    'release_date': fields.Date(example='2013-09-12'),
    'rating': fields.Float(example='9.5'),
    'genres': fields.String(example=[
        {
            "genre_name": "Action"
        },
        {
            "genre_name": "Comedy"
        },
        {
            "genre_name": "Fantasy"
        }
    ]),
    'directors': fields.String(example=[
        {
            "name": "Deanna",
            "surname": "Craig"
        },
        {
            "name": "Michaela",
            "surname": "Ruiz"
        }
    ])
})


@film_ns.route('/<int:film_id>', methods=['GET', 'PUT', 'DELETE'], endpoint='film')
@film_ns.route('', methods=['POST'], endpoint='film_create')
class FilmBase(Resource):
    """Class for implementing film HTTP requests"""
    @film_ns.response(200, 'Success')
    @film_ns.response(404, 'Not Found')
    @film_ns.doc(params={'film_id': 'An ID'})
    def get(self, film_id):
        """Get one record from the film table"""
        film_rec = todo.get(record_id=film_id, crud=film, t_name='film')
        return set_unknown_director(film_rec)

    @film_ns.response(201, 'Created', model=film_model)
    @film_ns.response(401, 'Unauthorized')
    @film_ns.response(400, 'Validation Error')
    @film_ns.doc(body=film_create_model)
    def post(self):
        """Create new record in the film table"""
        if not current_user.is_authenticated:
            logger.error('An attempt to add a movie by an unauthenticated user.')
            film_ns.abort(401, 'You need to be authenticated to add a film')
        directors_id = request.json.get('directors')
        genres_id = request.json.get('genres')
        values = {
            'title': request.json.get('title'),
            'poster': request.json.get('poster'),
            'description': request.json.get('description'),
            'release_date': request.json.get('release_date'),
            'rating': request.json.get('rating'),
            'user_id': current_user.user_id
        }

        if values['description'] == '':
            values['description'] = 'Film has no description.'

        try:
            film_record = create_film(film, values=values,
                                      directors_id=directors_id,
                                      genres_id=genres_id)

            logger.info('Created new film with such fields\n%s.', str(values))
            return film_record, 201

        except (ValidationError, DataError) as error:
            logger.error("Incorrect data entered. "
                         "The record in film table could not be created. %s", error)
            film_ns.abort(400, message="Incorrect data entered. The record could not be created.")

        except ValueError:
            logger.error("Attempt to create film with title that already exist.")
            film_ns.abort(400, "Film with such title already exist.")

    def del_put_access(self, film_id: int, action: str):
        """Check access to put and post methods"""
        if not current_user.is_authenticated:
            logger.error('An attempt to %s a movie by an unauthenticated user.', action)
            film_ns.abort(401, f'You need to be authenticated to {action} a film.')
        db_film = Film.query.get(film_id)
        admin = Role.query.filter_by(name='admin').first()
        if db_film.user_id != current_user.user_id and current_user.role_id != admin.role_id:
            logger.error("Not the user who added the film and not an administrator "
                         "try to %s a film. Access denied.", action)
            film_ns.abort(403, "Only the user who added the film or an administrator "
                               "can make changes to a film. Access denied.")
        return True

    @film_ns.doc(model=film_model, body=film_update_model)
    @film_ns.doc(params={'film_id': 'An ID'})
    @film_ns.response(200, 'Successfully update')
    @film_ns.response(401, 'Unauthorized')
    @film_ns.response(403, 'Forbidden')
    @film_ns.response(404, 'Not Found')
    def put(self, film_id):
        """Update a record in the film table"""
        try:
            access = self.del_put_access(film_id=film_id, action='update')
            if access is True:
                film_rec = todo.update(record_id=film_id, crud=film, t_name='film')
                return set_unknown_director(film_rec)
            return access

        except AttributeError:
            logger.error('Attempt to update record with id %d in film table, '
                         'but record does not exist.', film_id)
            film_ns.abort(404, message=f"Record with id {film_id} doesn't exist.")

        except ValueError:
            logger.error("Attempt to update film title to the one that is already in the database.")
            film_ns.abort(400, "Film with such title already exist.")

    @film_ns.doc(params={'film_id': 'An ID'})
    @film_ns.response(204, 'Record deleted successfully')
    @film_ns.response(401, 'Unauthorized')
    @film_ns.response(403, 'Forbidden')
    @film_ns.response(404, 'Not Found')
    def delete(self, film_id):
        """Delete a record from the film table"""
        try:
            access = self.del_put_access(film_id=film_id, action='delete')
            if access is True:
                return todo.delete(record_id=film_id, crud=film, t_name='film')
            return access
        except (AttributeError, ValidationError):
            logger.error('Attempt to delete record with id %d in film table, '
                         'but record does not exist.', film_id)
            film_ns.abort(404, message=f"Record with id {film_id} doesn't exist.")


@film_ns.route('/all/<int:page>', methods=['GET'],
               defaults={'per_page': 10}, endpoint='films_default')
@film_ns.route('/all/<int:page>/<int:per_page>', methods=['GET'], endpoint='films')
@film_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page'})
class Films(Resource):
    """Class for implementing films get multy request"""
    @film_ns.response(200, 'Success')
    @film_ns.response(404, 'Not Found')
    def get(self, page, per_page):
        """Get all records from the film table"""
        try:
            films = read_films(crud=film, page=page, per_page=per_page).dict()
            logger.info('Returned the %d page of film table '
                        'records paginated with %d records per page.', page, per_page)
            return jsonify(set_unknown_director_multy(films)['__root__'])
        except NotFound:
            logger.warning("No more records in film table.")
            film_ns.abort(404, message=f"No more records in film table.")


@film_ns.route('/<string:title>/<int:page>', methods=['GET'],
               defaults={'per_page': 10}, endpoint='films_title_default')
@film_ns.route('/<string:title>/<int:page>/<int:per_page>', methods=['GET'],
               endpoint='films_title')
@film_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page',
                     'title': "Part of the film's title"})
class FilmsTitle(Resource):
    """Class for implementing films get multy request"""
    @film_ns.response(200, 'Success')
    @film_ns.response(404, 'Not Found')
    def get(self, page, per_page, title):
        """Get all records from the film table by partial coincidence of title"""
        try:
            films = get_multi_by_title(film_crud=film, page=page,
                                       per_page=per_page, title=title).dict()
            logger.info('Returned the %d page of film table '
                        'records paginated with %d records per page '
                        'by partial coincidence of the name with "%s"',
                        page, per_page, title)
            return jsonify(set_unknown_director_multy(films)['__root__'])
        except NotFound:
            logger.warning("No more records corresponding to the request in film table.")
            film_ns.abort(404, message=f"No more records corresponding "
                                       f"to the request in film table.")


@film_ns.route('/filter/<int:page>', methods=['GET'],
               defaults={'per_page': 10}, endpoint='films_filter_default')
@film_ns.route('/filter/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_filter')
@film_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page',
                     'release_date': {'description': 'Release year range', 'example': '2002-2020'},
                     'directors': {'description': 'Names and surnames of directors',
                                   'example': 'Ricky_Perkins&Mark_Hunter — if several directors or'
                                              ' Ricky_Perkins — if only one director'},
                     'genres': {'description': 'Genre names',
                                'example': 'Action&Comedy — if several genres or '
                                           'Comedy — if only one genre'}})
class FilmsFiltered(Resource):
    """Class for implementing films get multy filtered request"""
    @film_ns.response(200, 'Success')
    @film_ns.response(404, 'Not Found')
    def get(self, page, per_page):
        """Get all records from the film table filtered by genres, release_date and directors"""
        data = [request.args.get('release_date', default=None),
                request.args.get('directors', default=None),
                request.args.get('genres', default=None)]
        try:
            films = query_film_multy_filter(film_crud=film, values=data,
                                            page=page, per_page=per_page).dict()
            logger.info('Returned the %d page of film table '
                        'records paginated with %d records per page '
                        'filtered by "%s"', page, per_page, str(data))
            return jsonify(set_unknown_director_multy(films)['__root__'])
        except NotFound:
            logger.warning("No more records corresponding to the request in film table.")
            film_ns.abort(404, message=f"No more records corresponding "
                                       f"to the request in film table.")


@film_ns.route('/sort/<int:page>', methods=['GET'],
               defaults={'per_page': 10}, endpoint='films_sort_default')
@film_ns.route('/sort/<int:page>/<int:per_page>', methods=['GET'], endpoint='films_sort')
@film_ns.doc(params={'page': 'Page number', 'per_page': 'Number of entries per page',
                     'release_date': {'description': 'Sort order by release date',
                                      'example': 'asc — for ascending order, '
                                                 'desc — for descending'},
                     'rating': {'description': 'Sort order by rating',
                                'example': 'asc — for ascending order, desc — for descending'}})
class FilmsSorted(Resource):
    """Class for implementing films get multy sorted request"""
    @film_ns.response(200, 'Success')
    @film_ns.response(404, 'Not Found')
    def get(self, page: int, per_page: int):
        """Get all records from the film table sorted by release_date and rating"""
        order = [request.args.get('release_date', default=None),
                 request.args.get('rating', default=None)]
        try:
            films = query_film_multy_sort(film_crud=film, page=page,
                                          per_page=per_page, order=order).dict()
            logger.info('Returned the %d page of film table '
                        'records paginated with %d records per page '
                        'sorted by %s', page, per_page, str(order))
            return jsonify(set_unknown_director_multy(films)['__root__'])
        except NotFound:
            logger.warning("No more records corresponding to the request in film table.")
            film_ns.abort(404, message=f"No more records corresponding "
                                       f"to the request in film table.")
