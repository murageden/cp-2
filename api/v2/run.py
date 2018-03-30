"""/run.py."""
import os

from we_connect import create_app

config_name = os.getenv('APP_CONFIGURATION')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
