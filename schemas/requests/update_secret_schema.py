from marshmallow import validate, fields

from schemas.requests.get_secret_schema import GetSecretSchema


class UpdatedSecretSchema(GetSecretSchema):
    """ Schema for updating a secret """

    secret = fields.String(required=True, validate=validate.Length(min=1, max=1000000))
    password = fields.String(required=False, validate=validate.Length(min=1, max=32))
    create_on = fields.DateTime(required=False)
