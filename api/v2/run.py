"""/run.py."""
import os
from flask_sqlalchemy import SQLAlchemy

from we_connect import create_app

# initialize sql-alchemy
db = SQLAlchemy()

config_name = os.getenv('APP_CONFIGURATION') or 'testing'
app = create_app(config_name)

db.init_app(app)

if __name__ == '__main__':
    app.run()
