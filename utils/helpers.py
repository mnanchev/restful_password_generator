from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

from constants import NOT_EXISTING, REQUIRED_KEYS
from db import db
from managers.auth import AuthManager, auth


def check_if_query_is_valid(query):
    """
    Check if the query is valid
    :param query:
    :return:
    """
    if not query:
        raise NotFound(NOT_EXISTING)


def check_if_user_has_permissions_over_resource(query):
    """
    Check if the user has permissions over the resource
    :param query:
    :return: NotFound if the user doesn't have permissions over the resource
    """
    user_id = AuthManager.decode_token(auth.get_auth()["token"])[0]
    try:
        user_id_query = query.first().creator_id
        if not query or not user_id == user_id_query:
            raise NotFound(NOT_EXISTING)
    except AttributeError:
        raise NotFound(NOT_EXISTING)


def remove_not_required_model_keys(user_data):
    """
    Remove not required keys from the user data
    :param user_data:
    :return: cleaned user data without the not required keys
    """
    cleaned_user_data = {}
    for key in REQUIRED_KEYS:
        if key in user_data:
            cleaned_user_data[key] = user_data[key]
    return cleaned_user_data


def flush_db():
    """
    Flush the database
    :return: None if the database is flushed
    """
    try:
        db.session.flush()
    except IntegrityError:
        raise BadRequest("Duplicated key error")
