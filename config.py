from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class DevApplicationConfiguration:
    debug = False
    testing = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


def create_app(configuration="config.DevApplicationConfiguration"):
    app = Flask(__name__)
    app.config.from_object(configuration)
    Migrate(app, db)
    api = Api(app)
    CORS(app)
    [api.add_resource(*route) for route in routes]
    return app
