from flask import request
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    """
    Validate the request data against a schema
    :param schema_name:
    :return: BadRequest if the data is not valid and the function is called otherwise
    """

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


def validate_attached_file_schema(schema_name):
    """
    Validate the request data against a schema
    :param schema_name:
    :return: BadRequest if the data is not valid and the function is called otherwise
    """

    def wrapper(func):
        def decorated_func(*args, **kwargs):
            schema = schema_name()
            files = request.files
            errors = schema.validate(files)
            if errors:
                raise BadRequest("No file part")
            return func(*args, **kwargs)

        return decorated_func

    return wrapper


def validate_arguments(schema_name):
    """
    Validate the request arguments against a schema
    :param schema_name:
    :return: BadRequest if the data is not valid and the function is called otherwise
    """

    def wrapper(func):
        def decorated_func(*args, **kwargs):
            schema = schema_name()
            data = request.view_args
            errors = schema.validate(data)
            if errors:
                raise BadRequest(f"{errors}")
            return func(*args, **kwargs)

        return decorated_func

    return wrapper
