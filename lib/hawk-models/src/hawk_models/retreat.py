from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from hawk_db.retreat import RetreatItem, RetreatItemState, RetreatItemType
from hawk_models.base import ApiModelABC, ObjectSchema
from typing_extensions import TypedDict
from webargs import fields


class RetreatApiModel(ApiModelABC):
    def __init__(
        self,
        id: int,
        company_id: int,
        name: Optional[str] = None,
        retreat_items: List[object] = [],
        employee_location_submission: RetreatEmployeeLocationSubmissionModel = None,
    ):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.retreat_items = retreat_items
        self.employee_location_submissions = employee_location_submission

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            company_id = fields.Int(required=True)
            name = fields.Str()
            retreat_items = fields.Nested("RetreatToItemApiModelSchema", many=True)
            employee_location_submission = fields.Function(
                serialize=lambda obj: RetreatEmployeeLocationSubmissionSchema.dump(
                    obj=obj.employee_location_submissions[0]
                )
                if obj.employee_location_submissions
                else None
            )

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
        uid: str,
        type: RetreatItemType,
        data: Dict,
        title: str,
        subtitle: Optional[str] = None,
    ):
        self.id = id
        self.uid = uid
        self.type = type
        self.data = data
        self.title = title
        self.subtitle = subtitle

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatItemApiModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True)
            uid = fields.String(required=True)
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


class RetreatEmployeeLocationItemModel(ApiModelABC):
    def __init__(
        self,
        employee_count: int,
        google_place_id: str,
        main_text: str,
        secondary_text: str,
        id: int = None,
        submission_id: int = None,
    ):
        self.id = id
        self.submission_id = submission_id
        self.employee_count = employee_count
        self.google_place_id = google_place_id
        self.main_text = main_text
        self.secondary_text = secondary_text

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatEmployeeLocationItemModelSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True, dump_only=True)
            submission_id = fields.Int(required=True, dump_only=True)
            employee_count = fields.Int(required=True)
            google_place_id = fields.String(required=True)
            main_text = fields.String(required=True)
            secondary_text = fields.String(required=True)

        return RetreatEmployeeLocationItemModelSchema()


RetreatEmployeeLocationItemModelSchema = RetreatEmployeeLocationItemModel.Schema()


class RetreatEmployeeLocationSubmissionModel(ApiModelABC):
    def __init__(
        self,
        location_items: RetreatEmployeeLocationItemModel,
        id: int = None,
        retreat_id: int = None,
        created_at: Optional[datetime] = None,
        extra_info: Optional[str] = None,
    ):
        self.id = id
        self.retreat_id = retreat_id
        self.location_items = location_items
        self.created_at = created_at
        self.extra_info = extra_info

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatEmployeeLocationSubmissionSchema(ObjectSchema):
            __model__ = cls

            id = fields.Int(required=True, dump_only=True)
            retreat_id = fields.Int(required=True, dump_only=True)
            location_items = fields.Nested(
                "RetreatEmployeeLocationItemModelSchema", many=True
            )
            created_at = fields.AwareDateTime()
            extra_info = fields.String()

        return RetreatEmployeeLocationSubmissionSchema()


RetreatEmployeeLocationSubmissionSchema = (
    RetreatEmployeeLocationSubmissionModel.Schema()
)


# DEPRECATED IN FAVOR OF NEW MODELS
class MatchedSubstring(TypedDict):
    offset: int
    length: int


class StructuredFormatting(ApiModelABC):
    def __init__(
        self,
        main_text: str,
        secondary_text: Optional[str] = None,
        main_text_matched_substrings: Optional[MatchedSubstring] = None,
    ):
        self.main_text = main_text
        self.main_text_matched_substrings = main_text_matched_substrings
        self.secondary_text = secondary_text

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class StructuredFormattingSchema(ObjectSchema):
            __model__ = cls
            main_text = fields.String(required=True)
            main_text_matched_substrings = fields.List(fields.Dict(), load_only=True)
            secondary_text = fields.String(required=False)

        return StructuredFormattingSchema()


StructuredFormattingSchema = StructuredFormatting.Schema()


class GooglePlaceModel(ApiModelABC):
    def __init__(
        self,
        place_id: str,
        reference: str,
        description: str,
        structured_formatting: StructuredFormatting,
        terms: List[dict] = [],
        types: List[str] = [],
        matched_substrings: List[MatchedSubstring] = [],
    ):
        self.place_id = place_id
        self.reference = reference
        self.description = description
        self.terms = terms
        self.types = types
        self.structured_formatting = structured_formatting
        self.matched_substrings = matched_substrings

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class GooglePlaceModelSchema(ObjectSchema):
            __model__ = cls
            place_id = fields.String(required=True)
            reference = fields.String(required=True)
            description = fields.String(required=True)
            terms = fields.List(fields.Dict())
            types = fields.List(fields.String())
            structured_formatting = fields.Nested(
                "StructuredFormattingSchema", required=True
            )
            matched_substrings = fields.List(
                fields.Dict(), load_only=True, required=False
            )

        return GooglePlaceModelSchema()


GooglePlaceModelSchema = GooglePlaceModel.Schema()


class RetreatEmployeeLocationModel(ApiModelABC):
    def __init__(
        self,
        number: int,
        location: GooglePlaceModel,
    ):
        self.number = number
        self.location = location

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatEmployeeLocationModelSchema(ObjectSchema):
            __model__ = cls

            number = fields.Int(required=True)
            location = fields.Nested("GooglePlaceModelSchema", required=True)

        return RetreatEmployeeLocationModelSchema()


RetreatEmployeeLocationModelSchema = RetreatEmployeeLocationModel.Schema()


class RetreatToItemDataModel(ApiModelABC):
    def __init__(
        self,
        locations: List[RetreatEmployeeLocationModel],
        extra_info: Optional[str] = None,
        version: str = "1.0",
    ):
        self.locations = locations
        self.extra_info = extra_info
        self.version = version

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatToItemDataModelSchema(ObjectSchema):
            __model__ = cls

            extra_info = fields.String(required=False)
            locations = fields.Nested(
                "RetreatEmployeeLocationModelSchema", many=True, required=True
            )
            version = fields.String(required=False)

        return RetreatToItemDataModelSchema()


RetreatEmployeeLocationModelSchema = RetreatEmployeeLocationModel.Schema()


class RetreatEmployeeData(ApiModelABC):
    def __init__(
        self,
        locations: List[RetreatEmployeeLocationModel],
        timestamp: datetime,
        extra_info: Optional[str] = None,
        version: str = "1.0",
    ):
        self.locations = locations
        if extra_info:
            self.extra_info = extra_info
        self.timestamp = timestamp
        self.version = version

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatEmployeeDataSchema(ObjectSchema):
            __model__ = cls
            locations = fields.Nested(
                "RetreatEmployeeLocationModelSchema", many=True, required=True
            )
            extra_info = fields.String(required=False)
            version = fields.String(required=True)
            timestamp = fields.AwareDateTime(required=True)

        return RetreatEmployeeDataSchema()


RetreatEmployeeDataSchema = RetreatEmployeeData.Schema()


class RetreatEmployeeDataModel(ApiModelABC):
    def __init__(self, submissions: List[RetreatEmployeeData] = []):
        self.submissions = submissions

    @classmethod
    def Schema(cls) -> ObjectSchema:
        class RetreatEmployeeDataModelSchema(ObjectSchema):
            __model__ = cls

            submissions = fields.Nested(
                "RetreatEmployeeDataSchema", many=True, required=True
            )

        return RetreatEmployeeDataModelSchema()


RetreatEmployeeDataModelSchema = RetreatEmployeeDataModel.Schema()
