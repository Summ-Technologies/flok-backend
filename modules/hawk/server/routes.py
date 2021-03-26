from flask_restful import Api

from .controllers import auth, retreat, user

V1_PREFIX = "/v1."
V2_PREFIX = "/v2."


def route_v1(path: str, minor: int = 0):
    return "/api" + V1_PREFIX + str(minor) + path


def route_v2(path: str, minor: int = 0):
    return "/api" + V2_PREFIX + str(minor) + path


def route(path: str, version: str):
    return "/api/v" + version + path


def add_routes(api: Api):
    # Auth
    api.add_resource(auth.AuthSigninController, route_v1("/auth/signin"))
    api.add_resource(auth.AuthSignupController, route_v1("/auth/signup"))
    api.add_resource(auth.AuthResetController, route_v1("/auth/reset"))

    # User
    api.add_resource(user.UserHomeController, route_v1("/user/home"))

    # Retreat
    api.add_resource(
        retreat.RetreatController,
        route_v1("/retreats/<int:id>"),
    )
    api.add_resource(
        retreat.RetreatEmployeeLocationV2Controller,
        route_v1("/retreats/<int:id>/employees-locations"),
    )
    api.add_resource(
        retreat.RetreatEmployeeLocationController,
        route_v1("/retreats/<int:id>/<int:item_id>"),
    )  # DEPRECATED in favor of /retreats/:id/employee-locations
