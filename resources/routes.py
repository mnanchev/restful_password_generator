from resources.auth import Register, Login
from resources.s3_upload import S3Upload
from resources.secret import Secret
from resources.secret_detail import SecretDetail

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (Secret, "/generateSecret"),
    (
        SecretDetail,
        "/getSecret/<string:secret_id>",
        "/putSecret/<string:secret_id>",
        "/deleteSecret/<string:secret_id>",
    ),
    (S3Upload, "/upload"),
)
