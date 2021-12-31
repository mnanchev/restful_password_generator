from flask_restful import Resource

from managers.secret import SecretManager


class SecretDetail(Resource):
    def get(self, secret_id):
        secret_id = str(secret_id)
        return {"secret": SecretManager.get_secret(secret_id)}, 200
