from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    """ Marshmallow field for FileStorage objects. """

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if not isinstance(value, FileStorage):
            self.fail("Not a valid file.")

        return value


class S3UploadSchema(Schema):
    """ Schema for S3 upload requests. """

    file = FileStorageField(required=True, description="File name and path")
