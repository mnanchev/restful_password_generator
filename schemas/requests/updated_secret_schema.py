from marshmallow import validate, Schema, fields


class UpdatedSecretSchema(Schema):
    secret = fields.String(required=True, validate=validate.Length(min=1, max=1000000))
    password = fields.String(required=False, validate=validate.Length(min=1, max=32))
    create_on = fields.DateTime(required=False)
