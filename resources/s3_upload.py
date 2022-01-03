from flask_restful import Resource

from managers.auth import auth
from managers.s3_upload import S3UploadManager
from schemas.requests.s3_generate_upload_url_schema import S3GenerateUploadUrlSchema
from schemas.requests.s3_upload_schema import S3UploadSchema
from utils.decorators import validate_attached_file_schema, validate_schema


class S3Upload(Resource):
    """ S3Upload class """

    def __init__(self):
        self.s3_upload_manager = S3UploadManager()

    @auth.login_required
    @validate_attached_file_schema(S3UploadSchema)
    def post(self):

        url = self.s3_upload_manager.upload_file()
        return {"message": "File uploaded successfully", "url": url}, 201

    @auth.login_required
    @validate_schema(S3GenerateUploadUrlSchema)
    def get(self):
        url = self.s3_upload_manager.get_upload_url()
        return {"message": "Upload url generated successfully", "url": url}, 200
