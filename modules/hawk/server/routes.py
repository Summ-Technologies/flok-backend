from flask_restful import Api

from .controllers import auth, payment, retreat, user

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

    # # Payment
    api.add_resource(
        payment.CheckoutRetreatController,
        route_v1("/checkout/retreats"),
    )

    # Retreat
    api.add_resource(
        retreat.RetreatEmployeeLocationV2Controller,
        route_v1("/retreats/<int:retreat_id>/employees-locations"),
    )
    api.add_resource(
        retreat.RetreatFilterDetailsController,
        route_v1("/retreats/<int:retreat_id>/details"),
    )
    api.add_resource(
        retreat.RetreatProposalSelectedController,
        route_v1("/retreats/<int:retreat_id>/proposals/selected"),
    )
