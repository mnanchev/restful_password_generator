import uuid

from flask import request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Forbidden
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import auth, AuthManager
from models import SecretModel
from services.secrets_manager_service import SecretsManagerService
from utils.helpers import (
    check_if_query_is_valid,
    check_if_user_has_permissions_over_resource,
    remove_not_required_model_keys,
    flush_db,
)

SECRETS_MANAGER_SERVICE = SecretsManagerService()


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
        user_data = remove_not_required_model_keys(user_data)
        user_data["id"] = str(uuid.uuid4())
        secret = SecretModel(**user_data)
        db.session.add(secret)
        flush_db()
        return secret.id

    @staticmethod
    def get_secret(secret_id):
        secret_query = SecretModel.query.filter_by(id=secret_id).first()
        check_if_query_is_valid(secret_query)
        is_password_protected = secret_query.is_password_protected
        user_data = request.get_json()
        password = secret_query.password
        if is_password_protected and (
            (not user_data or "password" not in user_data)
            or (not check_password_hash(password, user_data["password"]))
        ):
            raise Forbidden("You do not have access to this resource")
        db.session.delete(secret_query)
        flush_db()
        return secret_query.secret

    @staticmethod
    def update_secret(user_data, secret_id):
        secret_query = SecretModel.query.filter_by(id=secret_id)
        check_if_query_is_valid(secret_query)
        check_if_user_has_permissions_over_resource(secret_query)
        secret_query.update(user_data)
        db.session.add(secret_query.first())
        flush_db()
        return secret_query

    @staticmethod
    def delete_secret(secret_id):
        secret_query = SecretModel.query.filter_by(id=secret_id)
        check_if_query_is_valid(secret_query)
        check_if_user_has_permissions_over_resource(secret_query)
        db.session.delete(secret_query.first())
        try:
            db.session.flush()
        except IntegrityError:
            raise BadRequest("Duplicated key error")
