from flask_restful import Api

from .controllers import auth, user

V1_PREFIX = "/v1.0"


def route_v1(path: str):
    return "/api" + V1_PREFIX + path


def route(path: str, version: str):
    return "/api/v" + version + path


def add_routes(api: Api):
    # Auth
    api.add_resource(auth.AuthSigninController, route_v1("/auth/signin"))
    api.add_resource(auth.AuthSignupController, route_v1("/auth/signup"))

    # User
    api.add_resource(user.UserHomeController, route_v1("/user/home"))
