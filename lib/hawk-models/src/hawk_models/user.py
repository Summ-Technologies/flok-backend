from hawk_models.base import ApiModelABC, ObjectSchema
from webargs import fields


class UserApiModel(ApiModelABC):
    def __init__(self, id: int, email: str, first_name: str, last_name: str):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class UserApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            email = fields.Str(required=True)
            first_name = fields.Str(required=True)
            last_name = fields.Str(required=True)

        return UserApiModelSchema()


UserApiModelSchema = UserApiModel.Schema()
