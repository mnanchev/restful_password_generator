from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.creator import CreatorModel


class UserManager:
    @staticmethod
    def register(user_data):
        user_data["password"] = generate_password_hash(user_data["password"])
        user = CreatorModel(**user_data)
        db.session.add(user)
        db.session.flush()

    @staticmethod
    def login(user_data):
        user = CreatorModel.query.filter_by(email=user_data["email"]).first()
        if not user or not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Wrong email or password")

        return user
