import logging

from flask_restful import Resource
from summ_web import responses

logger = logging.getLogger(__name__)


class HelloController(Resource):
    def get(self):
        return responses.success({"message": "Hello world!"})
