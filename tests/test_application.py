import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import CreatorFactory


class TestApp(TestCase):
    """
    Test the application
    """

    HEADERS = {"Content-Type": "application/json"}
    REGISTER_PATH = "/register"
    GENERATE_SECRET_PATH = "/generateSecret"

    def create_app(self):
        """
        Create the application
        :return:
        """
        return create_app()

    def setUp(self):
        """
        Create the database
        :return:
        """
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        """
        Drop the database
        :return:
        """
        db.session.remove()
        db.drop_all()

    def test_protected(self):
        """
        Test the protected route
        """
        for method, url in [
            ("POST", self.GENERATE_SECRET_PATH),
            ("PUT", "/putSecret/1"),
            ("GET", "/get_upload_url"),
            ("DELETE", "/deleteSecret/1"),
        ]:
            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}),)
            elif method == "GET":
                resp = self.client.get(url)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}),)
            else:
                resp = self.client.delete(url)
            self.assert401(resp, {"message": "Invalid token"})

    def test_register(self):
        """
        Test the register route
        """
        creator = CreatorFactory()
        resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.assertEqual(201, resp.status_code, {"message": "User created"})

    def test_login(self):
        """
        Test the login route
        """
        creator = CreatorFactory()
        self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        resp = self.client.post(
            "/login",
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.assertEqual(200, resp.status_code, {"message": "Success"})

    def test_login_wrong_password(self):
        """
        Test login with wrong password
        :return:
        """
        creator = CreatorFactory()
        resp = self.client.post(
            "/login",
            data=json.dumps(
                {"email": creator.email, "password": creator.password + "wrong"}
            ),
            headers=self.HEADERS,
        )
        self.assertEqual(400, resp.status_code, {"message": "Wrong email or password"})

    def test_generate_secret(self):
        """
        Test the generate secret route
        """
        creator = CreatorFactory()

        resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.HEADERS["Authorization"] = f"Bearer {resp.json['token']}"
        resp = self.client.post(
            self.GENERATE_SECRET_PATH,
            data=json.dumps(
                {
                    "PasswordLength": 255,
                    "ExcludeCharacters": "",
                    "ExcludeNumbers": False,
                    "ExcludePunctuation": True,
                    "ExcludeUppercase": True,
                    "ExcludeLowercase": True,
                    "IncludeSpace": False,
                    "password": "pesho",
                }
            ),
            headers=self.HEADERS,
        )
        self.assertEqual(201, resp.status_code)

    def test_generate_secret_without_token(self):
        """
        Test the generate secret route
        """
        self.HEADERS["Authorization"] = f"Bearer eaas"
        resp = self.client.post(
            self.GENERATE_SECRET_PATH,
            data=json.dumps(
                {
                    "PasswordLength": 255,
                    "ExcludeCharacters": "",
                    "ExcludeNumbers": False,
                    "ExcludePunctuation": True,
                    "ExcludeUppercase": True,
                    "ExcludeLowercase": True,
                    "IncludeSpace": False,
                    "password": "pesho",
                }
            ),
            headers=self.HEADERS,
        )
        self.assertEqual(401, resp.status_code)

    def test_get_secret_with_predefined_secret(self):
        """
        Test the get secret route
        """
        # creator = CreatorFactory()
        # reg_resp = self.client.post(
        #     self.REGISTER_PATH,
        #     data=json.dumps({"email": creator.email, "password": creator.password}),
        #     headers=self.HEADERS,
        # )
        # secret = SecretFactory()
        # self.client.post(
        #     self.REGISTER_PATH,
        #     data=json.dumps({"email": creator.email, "password": creator.password}),
        #     headers=self.HEADERS,
        # )
        # resp = self.client.get(
        #     f"/getSecret/{secret.id}", headers=self.HEADERS
        # )
        # self.assertEqual(200, resp.status_code)
        # """
