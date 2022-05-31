"""Main app module"""

from flask import Flask
from config import Config
from models import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def index():
    """The function responsible for the content of the main page"""
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
