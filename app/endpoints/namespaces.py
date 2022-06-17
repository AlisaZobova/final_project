"""API namespaces module"""

from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

auth_ns = api.namespace('authentication', description='Authentication namespace')
api.add_namespace(auth_ns, path='/auth')

director_ns = api.namespace('director', description='Director namespace')
api.add_namespace(director_ns)

film_ns = api.namespace('film', description='Film namespace')
api.add_namespace(film_ns)

genre_ns = api.namespace('genre', description='Genre namespace')
api.add_namespace(genre_ns)

user_ns = api.namespace('user', description='User namespace')
api.add_namespace(user_ns)
