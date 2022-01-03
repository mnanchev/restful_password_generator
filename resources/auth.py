from flask_restful import Resource, request

from managers.auth import AuthManager
from managers.user import UserManager
from models.enums import RoleType
from schemas.requests.creator import CreatorSchema
from utils.decorators import validate_schema


class Register(Resource):
    """
    Register a new user
    """

    @validate_schema(CreatorSchema)
    def post(self):
        data = request.get_json()
        user = UserManager.register(data)
        token = AuthManager.encode_token(user)
        return {"message": "Success", "token": token}, 201


class Login(Resource):
    """
    Login a user
    """

    @validate_schema(CreatorSchema)
    def post(self):
        user = UserManager.login(request.get_json())
        token = AuthManager.encode_token(user)
        return (
            {
                "message": "Success",
                "token": token,
                "role": RoleType.SIGNED_CREATOR.value,
            },
            200,
        )
