from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from db import db
from resources.routes import routes


class DevApplicationConfiguration:
    Debug = True
    Testing = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


def create_app(config="config.DevApplicationConfiguration"):
    app = Flask(__name__)
    app.config.from_object(DevApplicationConfiguration)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)
    endpoints = [api.add_resource(*route) for route in routes]
    return app
