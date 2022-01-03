import inspect
import os
from unittest import TestCase

import boto3
from decouple import config
from loguru import logger
from moto.s3 import mock_s3

from constants import TEMP_FILE_FOLDER
from services.s3_service import S3Service


class TestS3Service(TestCase):
    """ Test S3Service class """

    @mock_s3
    def test_upload_object(self):
        """
        Test upload object to S3
        :return: url of the uploaded object
        """
        logger.debug(
            f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
        )
        s3_client = boto3.client("s3", region_name=config("AWS_REGION"))
        s3_client.create_bucket(
            Bucket=config("AWS_BUCKET"),
            CreateBucketConfiguration={"LocationConstraint": config("AWS_REGION")},
        )
        s3_service = S3Service()
        object_name = "index.jpg"
        path = os.path.join(TEMP_FILE_FOLDER, object_name)
        url = s3_service.upload_object(path, object_name, expiration_time=3600)
        assert url is not None and (
            "s3.amazonaws.com" and "https://" and f"{config('AWS_BUCKET')}" in url
        )
        logger.info(url)
