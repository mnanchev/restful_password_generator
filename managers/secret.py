import uuid

from flask import request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Forbidden
from werkzeug.security import generate_password_hash, check_password_hash

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
        user_data["id"] = str(uuid.uuid4())
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

    @staticmethod
    def get_secret(secret_id):
        query = SecretModel.query.filter_by(id=secret_id).first()
        is_password_protected = query.is_password_protected
        user_data = request.get_json()
        password = query.password
        if is_password_protected and (
            (not user_data or "password" not in user_data)
            or (not check_password_hash(password, user_data["password"]))
        ):
            raise Forbidden("You do not have access to this resource")
        return query.secret
