import uuid

import boto3
from botocore.exceptions import ClientError
from decouple import config
from loguru import logger
from werkzeug.exceptions import InternalServerError


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
        )

    def __generate_pre_signed_url(self, expiration_time, object_name):
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": f"{uuid.uuid4()}/{object_name}"},
            ExpiresIn=expiration_time,
        )
        return url

    def upload_object(self, file_name, object_name, expiration_time):
        try:
            self.s3.upload_file(
                file_name, self.bucket_name, object_name,
            )
            return self.__generate_pre_signed_url(expiration_time, object_name)
        except ClientError as client_error:
            logger.exception(
                "Provider is not available at the moment.\n Please try again later",
                client_error,
            )
            raise InternalServerError(
                "Provider is not available at the moment.\n Please try again later"
            )
