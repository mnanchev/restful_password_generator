from marshmallow import validate, Schema, fields


class SecretSchema(Schema):
    """ Secret schema """

    secret = fields.String(required=False, validate=validate.Length(min=1, max=1000000))
    password = fields.String(required=False, validate=validate.Length(min=1, max=32))
    ExcludeCharacters = fields.String(required=False)
    IncludeSpace = fields.Boolean(required=False)
    PasswordLength = fields.Integer(required=False)
    ExcludePunctuation = fields.Boolean(required=False)
    RequireEachIncludedType = fields.Boolean(required=False)
    ExcludeNumbers = fields.Boolean(required=False)
    ExcludeUppercase = fields.Boolean(required=False)
    ExcludeLowercase = fields.Boolean(required=False)
