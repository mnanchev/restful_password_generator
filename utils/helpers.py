from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

from db import db
from managers.auth import AuthManager, auth

REQUIRED_KEYS = ["secret", "password", "is_password_protected", "creator_id"]
NOT_EXISTING = "Secret does not exist"


def check_if_query_is_valid(query):
    if not query:
        raise NotFound(NOT_EXISTING)


def check_if_user_has_permissions_over_resource(query):
    user_id = AuthManager.decode_token(auth.get_auth()["token"])[0]
    try:
        user_id_query = query.first().creator_id
        if not query or not user_id == user_id_query:
            raise NotFound(NOT_EXISTING)
    except AttributeError:
        raise NotFound(NOT_EXISTING)


def remove_not_required_model_keys(user_data):
    cleaned_user_data = {}
    for key in REQUIRED_KEYS:
        if key in user_data:
            cleaned_user_data[key] = user_data[key]
    return cleaned_user_data


def flush_db():
    try:
        db.session.flush()
    except IntegrityError:
        raise BadRequest("Duplicated key error")
