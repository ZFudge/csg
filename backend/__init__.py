from flask import Flask
from flask_caching import Cache
from flask_socketio import SocketIO


cache = Cache()

app = Flask(
	__name__,
	root_path='/csg',
	static_folder='build',
	static_url_path='/'
)

cache.init_app(app, config={
	'CACHE_TYPE': 'FileSystemCache',
	'CACHE_DIR': '.flask_cache',
	# in seconds
	"CACHE_DEFAULT_TIMEOUT": 7200,
})

socket = SocketIO(
	app,
	cors_allowed_origins='*',
	logger=True,
	engineio_logger=True
)

from .views.main import main
app.register_blueprint(main)
from .views.session import session
app.register_blueprint(session)
from .views.gameplay import gameplay
app.register_blueprint(gameplay)
from .views.actions import misc
app.register_blueprint(misc)

if __name__ == '__main__':
	socket.run(app)
