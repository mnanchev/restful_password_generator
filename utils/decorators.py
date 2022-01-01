from flask import request
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    def wrapper(func):
        def decorated_func(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(f"{errors}")
            return func(*args, **kwargs)

        return decorated_func

    return wrapper


def check_if_file_attached(func):
    def decorated_func(*args, **kwargs):
        if not request.files:
            raise BadRequest("No file part")
        return func(*args, **kwargs)

    return decorated_func


def check_if_object_name_exists(func):
    def decorated_func(*args, **kwargs):
        user_data = request.get_json()
        if (not user_data) or ("object_name" not in user_data):
            raise BadRequest("No object name")
        return func(*args, **kwargs)

    return decorated_func
