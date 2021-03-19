from enum import Enum
from typing import Dict, List, Optional

from hawk_db.retreat import RetreatItem, RetreatItemState, RetreatItemType
from hawk_models.base import ApiModelABC, ObjectSchema
from webargs import fields


class RetreatApiModel(ApiModelABC):
    def __init__(
        self,
        id: int,
        company_id: int,
        name: Optional[str] = None,
        retreat_items: List[object] = [],
    ):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.retreat_items = retreat_items

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            company_id = fields.Int(required=True)
            name = fields.Str()
            retreat_items = fields.Nested("RetreatToItemApiModelSchema", many=True)

        return RetreatApiModelSchema()


RetreatApiModelSchema = RetreatApiModel.Schema()


class RetreatToItemApiModel(ApiModelABC):
    def __init__(
        self,
        retreat_id: int,
        retreat_item: RetreatItem,
        state: RetreatItemState,
        data: Dict,
        saved_data: Dict,
        order: int,
    ):
        self.order = order
        self.retreat_id = retreat_id
        self.retreat_item = retreat_item
        self.state = state
        self.data = data
        self.saved_data = saved_data

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatToItemApiModelSchema(ObjectSchema):
            __model__ = cls

            retreat_id = fields.Int(required=True)
            retreat_item = fields.Nested("RetreatItemApiModelSchema")
            state = fields.Str(required=True)
            data = fields.Dict(required=True)
            saved_data = fields.Dict(required=True)
            order = fields.Int(required=True)

        return RetreatToItemApiModelSchema()


RetreatToItemApiModelSchema = RetreatToItemApiModel.Schema()


class RetreatItemApiModel(ApiModelABC):
    def __init__(
        self,
        id: int,
        type: RetreatItemType,
        data: Dict,
        title: str,
        subtitle: Optional[str] = None,
    ):
        self.id = id
        self.type = type
        self.data = data
        self.title = title
        self.subtitle = subtitle

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatItemApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            type = fields.Str(required=True)
            data = fields.Dict(required=True)
            title = fields.Str(required=True)
            subtitle = fields.Str()

        return RetreatItemApiModelSchema()


RetreatItemApiModelSchema = RetreatItemApiModel.Schema()

TEMPLATES: Dict[str, List[str]] = {
    "V1.0": [
        "INTAKE_CALL-V1.0",
        "EMPLOYEE_LOCATIONS-V1.0",
        "INITIAL_PROPOSALS-V1.0",
        "DESTINATION_SELECTION-V1.0",
        "POST_PAYMENT-V1.0",
    ]
}
