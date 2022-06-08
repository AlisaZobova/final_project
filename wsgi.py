"""Main app module"""

from flask_cors import CORS
from app import create_app

app = create_app()  # pylint: disable=C0103
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
