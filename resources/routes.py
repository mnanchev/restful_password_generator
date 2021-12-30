from resources.auth import Register, Login
from resources.secret import Secret

routes = ((Register, "/register"), (Login, "/login"), (Secret, "/generateSecret"))
