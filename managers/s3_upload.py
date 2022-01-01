import os

from flask import request

from services.s3_service import S3Service


class S3UploadManager:
    @staticmethod
    def upload_file():
        s3_service = S3Service()
        file = request.files["file"]
        root_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_dir, file.filename)
        file.save(file_path)
        user_data = request.get_json()
        if user_data and "expiration_time" in user_data:
            s3_service.upload_object(
                file_path, file.filename, request.get_json()["expiration_time"]
            )
        else:
            url = s3_service.upload_object(file_path, file.filename, 3600)
        return url
