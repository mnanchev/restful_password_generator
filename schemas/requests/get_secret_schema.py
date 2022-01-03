from marshmallow import Schema, fields


class GetOrDeleteSecretArgumentsSchema(Schema):
    """ Schema for the arguments of the get_secret and delete_secret methods. """

    secret_id = fields.String(required=True, nullable=False)


class GetSecretSchema(Schema):
    """ Schema for the response of the get_secret method. """

    password = fields.String(required=False, nullable=False)
