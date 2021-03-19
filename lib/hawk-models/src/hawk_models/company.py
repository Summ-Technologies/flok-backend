from typing import Optional

from hawk_models.base import ApiModelABC, ObjectSchema
from webargs import fields


class CompanyApiModel(ApiModelABC):
    def __init__(self, id: int, name: Optional[str] = None):
        self.id = id
        self.name = name

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class CompanyApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            name = fields.Str(required=False)

        return CompanyApiModelSchema()


CompanyApiModelSchema = CompanyApiModel.Schema()
