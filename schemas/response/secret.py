from marshmallow import fields, Schema


class SecretResponseSchema(Schema):
    creator_id = fields.Integer()
    create_on = fields.DateTime()
    id = fields.String()
    secret = fields.String()
    is_password_protected = fields.Boolean()
    password = fields.String()
    creator = fields.String()
