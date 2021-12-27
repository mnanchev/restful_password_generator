import inspect
from unittest import TestCase

from loguru import logger
from moto import mock_secretsmanager

from services.secrets_manager_service import SecretsManagerService


class TestSecretsManagerService(TestCase):
    @mock_secretsmanager
    def test_get_random_password(self):
        logger.debug(
            f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
        )
        secrets_manager_service = SecretsManagerService()
        response = secrets_manager_service.get_random_password(
            {
                "PasswordLength": 16,
                "ExcludeCharacters": "",
                "ExcludeNumbers": False,
                "ExcludePunctuation": False,
                "ExcludeUppercase": False,
                "ExcludeLowercase": False,
                "IncludeSpace": True,
                "RequireEachIncludedType": True,
            }
        )
        password = response["RandomPassword"]
        assert len(password) == 16
        assert not password.isupper() and not password.islower()
        assert " " in password
        assert True in [character.isdigit() for character in password]
        logger.info(password)
