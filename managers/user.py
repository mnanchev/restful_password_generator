from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.creator import CreatorModel
from utils.helpers import flush_db


class UserManager:
    """
    User manager class
    """

    @staticmethod
    def register(user_data):
        """
        Register a new user
        :param user_data:
        :return: user: CreatorModel
        """
        user_data["password"] = generate_password_hash(user_data["password"])
        user = CreatorModel(**user_data)
        db.session.add(user)
        flush_db()
        return user

    @staticmethod
    def login(user_data):
        """
        Login a user
        :param user_data:
        :return: user: CreatorModel
        """
        user = CreatorModel.query.filter_by(email=user_data["email"]).first()
        if not user or not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Wrong email or password")

        return user
