from flask_restful import Api
from hawk_db import payment

from .controllers import webhook


def route(path: str, major: int = 1, minor: int = 0):
    return "/api" + f"/v{major}.{minor}" + path


def add_routes(api: Api):
    api.add_resource(webhook.WebhookController, route("/stripe/webhooks"))
