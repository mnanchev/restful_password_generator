import boto3
from botocore.exceptions import ClientError, ParamValidationError
from decouple import config
from loguru import logger
from werkzeug.exceptions import InternalServerError, BadRequest


class SecretsManagerService:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.region = config("AWS_REGION")
        self.secrets_manager_client = boto3.client(
            "secretsmanager",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )

    def get_random_password(self, password_params):
        try:

            response = self.secrets_manager_client.get_random_password(
                **password_params
            )
        except ClientError as client_error:
            if client_error.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.exception("Secret not found")
                raise BadRequest("Secret not found")
            elif client_error.response["Error"]["Code"] == "InvalidRequestException":
                logger.exception("The request was invalid due to:", client_error)
                raise BadRequest("Invalid request")
            elif client_error.response["Error"]["Code"] == "InvalidParameterException":
                logger.exception("The request had invalid params:", client_error)
                raise BadRequest("Invalid parameters f")
            else:
                logger.exception(
                    "Provider is not available at the moment.\n Please try again later",
                    client_error,
                )
                raise InternalServerError(
                    "Provider is not available at the moment.\n Please try again later"
                )
        except ParamValidationError as param_validation_error:
            raise BadRequest(str(param_validation_error))

        return response
