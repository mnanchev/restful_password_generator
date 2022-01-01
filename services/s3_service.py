import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from decouple import config
from loguru import logger
from werkzeug.exceptions import InternalServerError

from constants import NOT_AVAILABLE


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.bucket_name = config("AWS_BUCKET")
        self.region = config("AWS_REGION")
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region,
            config=Config(signature_version="s3v4"),
        )

    def __generate_pre_signed_url(
        self, expiration_time, object_name, key_prefix, operation_name="get_object"
    ):
        url = self.s3.generate_presigned_url(
            operation_name,
            Params={"Bucket": self.bucket_name, "Key": f"{key_prefix}/{object_name}"},
            ExpiresIn=expiration_time,
        )
        return url

    def upload_object(self, file_name, object_name, expiration_time):
        try:
            key_prefix = str(uuid.uuid4())
            self.s3.upload_file(
                file_name, self.bucket_name, f"{key_prefix}/{object_name}",
            )
            return self.__generate_pre_signed_url(
                expiration_time, object_name, key_prefix
            )
        except ClientError as client_error:
            logger.exception(
                NOT_AVAILABLE, client_error,
            )
            raise InternalServerError(NOT_AVAILABLE)

    def get_upload_url(self, expiration_time, object_name):
        try:
            key_prefix = str(uuid.uuid4())
            return self.__generate_pre_signed_url(
                expiration_time, object_name, key_prefix, "put_object"
            )
        except ClientError as client_error:
            logger.exception(
                NOT_AVAILABLE, client_error,
            )
            raise InternalServerError(NOT_AVAILABLE)
