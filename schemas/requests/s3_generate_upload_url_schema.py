from marshmallow import Schema, fields
from marshmallow.validate import Range


class S3GenerateUploadUrlSchema(Schema):
    """ S3GenerateUploadUrlSchema class """

    object_name = fields.String(required=True, description="File name and path")
    expiration_time = fields.Integer(validate=Range(min=1, max=604800))
