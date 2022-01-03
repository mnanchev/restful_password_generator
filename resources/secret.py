from decouple import config
from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.secret import SecretManager
from schemas.requests.secret import SecretSchema
from utils.decorators import validate_schema


class Secret(Resource):
    """ Secret resource """

    @auth.login_required
    @validate_schema(SecretSchema)
    def post(self):
        user_data = request.get_json()
        secret_params = {
            "PasswordLength": user_data.get("PasswordLength", 32),
            "ExcludeCharacters": user_data.get("ExcludeCharacters", ""),
            "ExcludeNumbers": user_data.get("ExcludeNumbers", False),
            "ExcludePunctuation": user_data.get("ExcludePunctuation", False),
            "ExcludeUppercase": user_data.get("ExcludeUppercase", False),
            "ExcludeLowercase": user_data.get("ExcludeLowercase", False),
            "IncludeSpace": user_data.get("IncludeSpace", False),
            "RequireEachIncludedType": user_data.get("RequireEachIncludedType", False),
        }
        req_id = SecretManager().create_secret(user_data, secret_params)
        return {"message": f"{config('DOMAIN')}/getSecret/{req_id}"}, 201
