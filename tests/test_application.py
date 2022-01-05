import json
from io import BytesIO

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
                    "password": creator.password,
                }
            ),
            headers=self.HEADERS,
        )
        self.assertEqual(201, resp.status_code)

    def test_generate_secret_without_token(self):
        """
        Test the generate secret route
        """
        self.HEADERS["Authorization"] = "Bearer eYiQqQ"
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
                    "password": self.HEADERS,
                }
            ),
            headers=self.HEADERS,
        )
        self.assertEqual(401, resp.status_code)

    def test_get_secret(self):
        """
        Test the get secret route
        """
        creator = CreatorFactory()

        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        gen_secret_resp = self.client.post(
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
                    "password": creator.password,
                }
            ),
            headers=self.HEADERS,
        )
        secret_id = gen_secret_resp.json["message"].split("/")[-1]
        resp = self.client.get(
            f"/getSecret/{secret_id}",
            headers=self.HEADERS,
            data=json.dumps({"password": creator.password}),
        )
        print(resp)
        self.assertEqual(200, resp.status_code)
        another_resp = self.client.get(
            f"/getSecret/{secret_id}",
            headers=self.HEADERS,
            data=json.dumps({"password": creator.password}),
        )
        print(another_resp)
        self.assertEqual(404, another_resp.status_code)

    def test_update_secret_with_predefined_secret(self):
        """
        Test the update secret route
        """
        creator = CreatorFactory()

        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        gen_secret_resp = self.client.post(
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
                    "password": creator.password,
                }
            ),
            headers=self.HEADERS,
        )
        secret_id = gen_secret_resp.json["message"].split("/")[-1]
        resp = self.client.put(
            f"/getSecret/{secret_id}",
            headers=self.HEADERS,
            data=json.dumps({"password": creator.password, "secret": "new secret"}),
        )
        self.assertEqual(200, resp.status_code)

    def test_delete_secret(self):
        """
        Test the delete secret route
        """
        creator = CreatorFactory()

        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        gen_secret_resp = self.client.post(
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
                    "password": creator.password,
                }
            ),
            headers=self.HEADERS,
        )
        secret_id = gen_secret_resp.json["message"].split("/")[-1]
        resp = self.client.delete(f"/deleteSecret/{secret_id}", headers=self.HEADERS,)
        self.assertEqual(204, resp.status_code)

    def test_s3_upload_object_without_file(self):
        """
        Test upload of object to S3
        """
        creator = CreatorFactory()

        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )
        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        resp = self.client.post("/upload", headers=self.HEADERS)
        self.assertEqual(400, resp.status_code)

    def test_s3_upload_object_with_file(self):
        """
        Test upload of object to S3
        """
        creator = CreatorFactory()
        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )

        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        data = {"test_file": "this is a test file"}
        data = {key: str(value) for key, value in data.items()}
        data["file"] = (BytesIO(b"abide"), "test.jpg")
        resp = self.client.post(
            "/upload",
            headers=self.HEADERS,
            content_type="multipart/form-data",
            data=data,
        )
        self.assertEqual(201, resp.status_code)

    def test_s3_generate_url_for_sharing_without_object_name(self):
        """
        Test generate of shared url for file upload from third parties
        """
        creator = CreatorFactory()
        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )

        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        resp = self.client.get("/upload", headers=self.HEADERS, data=json.dumps({}),)
        print(resp.json)
        self.assertEqual(400, resp.status_code)

    def test_s3_generate_url_for_sharing_with_object_name(self):
        """
        Test generate of shared url for file upload from third parties
        """
        creator = CreatorFactory()
        reg_resp = self.client.post(
            self.REGISTER_PATH,
            data=json.dumps({"email": creator.email, "password": creator.password}),
            headers=self.HEADERS,
        )

        self.HEADERS["Authorization"] = f"Bearer {reg_resp.json['token']}"
        resp = self.client.get(
            "/upload",
            headers=self.HEADERS,
            data=json.dumps({"object_name": "test.jpg"}),
        )
        self.assertEqual(200, resp.status_code)
