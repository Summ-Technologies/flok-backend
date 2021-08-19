from flask_restful import Api

from .controllers import auth, calendly, lodging, user

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
    api.add_resource(auth.AuthResetController, route_v1("/auth/reset"))

    # User
    api.add_resource(user.UserHomeController, route_v1("/user/home"))

    # Lodging
    api.add_resource(
        lodging.LodgingProposalRequestController, route_v1("/lodging/proposal-requests")
    )

    # Calendly webhook
    api.add_resource(calendly.CalendlyWebhookController, route_v1("/webhooks/calendly"))
