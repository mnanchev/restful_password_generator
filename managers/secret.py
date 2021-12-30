from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash

from db import db
from managers.auth import auth, AuthManager
from models import SecretModel
from services.secrets_manager_service import SecretsManagerService

SECRETS_MANAGER_SERVICE = SecretsManagerService()
REQUIRED_KEYS = ["secret", "password", "is_password_protected", "creator_id"]


class SecretManager:
    @staticmethod
    def create_secret(user_data, secret_params):
        if "secret" not in user_data.keys():
            secret = SECRETS_MANAGER_SERVICE.get_random_password(secret_params)
            user_data["secret"] = secret["RandomPassword"]
        if "password" in user_data.keys():
            user_data["is_password_protected"] = True
            user_data["password"] = generate_password_hash(user_data["password"])
        user_data["creator_id"] = AuthManager.decode_token(auth.get_auth()["token"])[0]
        user_data = SecretManager.__remove_not_required_model_keys(user_data)
        secret = SecretModel(**user_data)
        db.session.add(secret)
        try:
            db.session.flush()
        except IntegrityError:
            raise BadRequest("Duplicated key error")
        return secret.id

    @staticmethod
    def __remove_not_required_model_keys(user_data):
        cleaned_user_data = {}
        for key in REQUIRED_KEYS:
            if key in user_data:
                cleaned_user_data[key] = user_data[key]
        return cleaned_user_data
