from typing import Optional

from marshmallow import Schema, post_load
from webargs import fields


class ObjectSchema(Schema):
    """
    Object provides base class for all schemas to extend from.
    Stolen from https://marshmallow.readthedocs.io/en/stable/extending.html?highlight=__model__#example-enveloping
    """

    __model__ = None

    @post_load
    def make_object(self, data, **kwargs):
        assert self.__model__ is not None, "Model class is undefined"
        return self.__model__(**data)


class ApiModelABC:
    @classmethod
    def Schema(cls) -> ObjectSchema:
        raise Exception("LoginData type needs to implement Schema class method")
