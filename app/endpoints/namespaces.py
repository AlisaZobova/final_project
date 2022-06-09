"""API namespaces module"""

from flask import Blueprint
from flask_restx import Api

# pylint: disable=C0103

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

authentication = api.namespace('authentication', description='Authentication namespace')
api.add_namespace(authentication, path='/auth')

director = api.namespace('director', description='Director namespace')
api.add_namespace(director)

film = api.namespace('film', description='Film namespace')
api.add_namespace(film)

genre = api.namespace('genre', description='Genre namespace')
api.add_namespace(genre)

user = api.namespace('user', description='User namespace')
api.add_namespace(user)
