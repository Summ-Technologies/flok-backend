import enum
from typing import Optional

from marshmallow import fields

from .base import ObjectSchema


class UserLoginProviderType(enum.Enum):
    FLOK = "FLOK"


class LoginDataABC:
    @classmethod
    def Schema(cls) -> ObjectSchema:
        raise Exception("LoginData type needs to implement Schema class method")


class FlokLoginData(LoginDataABC):
    password: str

    def __init__(self, password: str):
        self.password = password  # encrypted pw when stored

    @classmethod
    def Schema(cls):
        class FlokLoginDataSchema(ObjectSchema):
            __model__ = cls

            password = fields.Str(required=True)

        return FlokLoginDataSchema


def get_login_data_serializer(
    login_provider_type: UserLoginProviderType,
) -> Optional[ObjectSchema]:
    """Get the login data serializer/deserializer given the login provider type"""
    serializer_mapping = {UserLoginProviderType.FLOK: FlokLoginData}
    model = serializer_mapping.get(UserLoginProviderType[login_provider_type.name])
    if model:
        return model.Schema()()
