from resources.auth import Register, Login
from resources.secret import Secret
from resources.secret_detail import SecretDetail

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (Secret, "/generateSecret"),
    (SecretDetail, "/getSecret/<string:secret_id>"),
)
