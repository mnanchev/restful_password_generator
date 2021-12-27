from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def wrapper(func):
        def decorated_func(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                raise BadRequest("...")
            return func(*args, **kwargs)

        return decorated_func

    return wrapper


def permission_required(permission):
    def wrapper(func):
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role == permission:
                raise Forbidden("You do not have access to this resource")
            return func(*args, **kwargs)

        return decorated_function

    return wrapper
