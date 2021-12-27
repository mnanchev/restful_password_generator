import uuid

from pynamodb.exceptions import PutError
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User


class UserManager:
    @staticmethod
    def register(user_data):
        user = User(
            user_data["email"],
            password=generate_password_hash(user_data["password"]),
            id=uuid.uuid4(),
        )
        try:
            user.save()
        except PutError as put_exception:
            raise InternalServerError(put_exception.msg)
        return user

    @staticmethod
    def login(user_data):
        user = User.query(user_data["email"], User.password.exists())
        if not user or not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Wrong email or password")
        return user
