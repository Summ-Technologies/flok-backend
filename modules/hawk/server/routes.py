from flask_restful import Api

from .controllers import hello

V1_PREFIX = "/v1.0"


def route_v1(path: str):
    return "/api" + V1_PREFIX + path


def route(path: str, version: str):
    return "/api/v" + version + path


def add_routes(api: Api):
    # Hello
    api.add_resource(hello.HelloController, route_v1("/hello-world"))
