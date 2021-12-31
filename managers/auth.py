from datetime import datetime, timedelta
from typing import Type

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest

from models import CreatorModel

RoleMapping: dict[str, Type[CreatorModel]] = {"CreatorModel": CreatorModel}


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=2),
            "role": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("JWT_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(jwt=token, key=config("JWT_KEY"), algorithms=["HS256"])
            return data["sub"], data["role"]
        except jwt.ExpiredSignatureError:
            raise BadRequest("Expired token")
        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)
    user = RoleMapping[role]
    return user
