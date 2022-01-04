from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from models import CreatorModel

RoleMapping = {"CreatorModel": CreatorModel}


class AuthManager:
    """
    AuthManager class
    """

    @staticmethod
    def encode_token(user):
        """
        The function takes a user and returns a token
        :param user:
        :return: token
        """
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=2),
            "role": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("JWT_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        """
        The function takes a token and returns a user
        :param token:
        :return: user
        """
        try:
            data = jwt.decode(jwt=token, key=config("JWT_KEY"), algorithms=["HS256"])
            return data["sub"], data["role"]
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Expired token")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    """
    The function takes a token and returns a user
    :param token:
    :return: user
    """
    user_id, role = AuthManager.decode_token(token)
    user = RoleMapping[role]
    return user
