"""Main app module"""

import os
from flask import Flask
from database import db_session


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route('/')
def index():
    """The function responsible for the content of the main page"""
    return 'OK'


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close the session after every request or application context termination"""
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
