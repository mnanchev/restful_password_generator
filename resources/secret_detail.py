from decouple import config
from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.secret import SecretManager
from schemas.requests.updated_secret_schema import (
    UpdatedSecretSchema,
    EmptySecretSchema,
)
from utils.decorators import validate_schema


class SecretDetail(Resource):
    @validate_schema(EmptySecretSchema)
    def get(self, secret_id):
        secret_id = str(secret_id)
        return {"message": f"{SecretManager.get_secret(secret_id)}"}, 200

    @auth.login_required
    @validate_schema(UpdatedSecretSchema)
    def put(self, secret_id):
        user_data = request.get_json()
        SecretManager().update_secret(user_data, secret_id)
        return {"message": f"{config('DOMAIN')}/getSecret/{secret_id}"}, 201

    @auth.login_required
    @validate_schema(EmptySecretSchema)
    def delete(self, secret_id):
        secret_id = str(secret_id)
        SecretManager().delete_secret(secret_id)
        return {"message": f"{secret_id} was removed"}, 204
