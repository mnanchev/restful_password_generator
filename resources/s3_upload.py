from flask_restful import Resource

from managers.auth import auth
from managers.s3_upload import S3UploadManager
from utils.decorators import check_if_file_exists


class S3Upload(Resource):
    @auth.login_required
    @check_if_file_exists
    def post(self):
        s3_upload_manager = S3UploadManager()
        url = s3_upload_manager.upload_file()
        return {"message": "File uploaded successfully", "url": url}, 201
