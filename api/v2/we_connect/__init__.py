"""we_connect/__init__.py."""
from flask_api import FlaskAPI

# local import
from instance.config import app_config


def create_app(config_name):
    """Configure and creates the app."""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app
