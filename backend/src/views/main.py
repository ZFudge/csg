from os import getenv

from dotenv import load_dotenv

from flask import Blueprint
from flask.helpers import send_from_directory
from werkzeug.routing import BaseConverter

from app import app

load_dotenv()
MAX_NAME_LENGTH = int(getenv('REACT_APP_MAX_NAME_LENGTH') or 10)
GAME_HASH_REGEX = getenv('REACT_APP_GAME_HASH_REGEX') or '[a-zA-Z0-9]'

main = Blueprint('main', __name__)

class GameHashConverter(BaseConverter):
    regex = f'{GAME_HASH_REGEX}' + '{' + f'{MAX_NAME_LENGTH}' + '}'
app.url_map.converters['game_hash'] = GameHashConverter

# use the converter in the route
@app.route('/join/<game_hash>')
@main.route('/')
@main.route('/new')
@main.route('/join')
@main.route('/game')
def serve(game_hash=''):
	"""Serve static files."""
	return send_from_directory(app.static_folder, 'index.html')
