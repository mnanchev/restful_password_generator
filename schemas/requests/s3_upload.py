from marshmallow import Schema, validate, fields


class S3UploadSchema(Schema):
    object_name = fields.String(validate=validate.Length(min=6, max=255))
    expiration_time = fields.String(validate=validate.Length(min=6, max=255))
