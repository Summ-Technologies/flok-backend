import logging

from flask import g
from flask_restful import Resource
from hawk_core.hawk_managers import LodgingManager, UserManager
from hawk_models.user import UserSchema
from marshmallow import ValidationError
from marshmallow.decorators import validates_schema
from marshmallow.schema import Schema
from summ_web import responses
from webargs import fields
from webargs.flaskparser import use_args

from .. import app, db, jwt

logger = logging.getLogger(__name__)

lodging_manager: LodgingManager = LodgingManager(db.session, app.config)


class LodgingProposalRequestPostSchema(Schema):
    email = fields.Email(required=True, data_key="email")
    company_name = fields.String(required=True, data_key="companyName")
    number_attendees = fields.Integer(min=0, data_key="numberAttendees")
    number_attendees_lower = fields.Integer(min=0, data_key="numberAttendeesLower")
    number_attendees_upper = fields.Integer(min=0, data_key="numberAttendeesUpper")
    meeting_spaces = fields.List(
        fields.String(),
        data_key="meetingSpaces",
        required=True,
    )
    occupancy_types = fields.List(
        fields.String(),
        data_key="occupancyTypes",
        required=True,
    )
    flexible_dates = fields.Boolean(required=True, data_key="flexibleDates")
    number_nights = fields.Integer(data_key="numberNights")
    preferred_months = fields.List(
        fields.String(),
        data_key="preferredMonths",
    )
    preferred_start_dow = fields.List(
        fields.String(),
        data_key="preferredStartDow",
    )
    start_date = fields.Date(data_key="startDate")
    end_date = fields.Date(data_key="endDate")

    @validates_schema
    def validate_fields(self, data, **kwargs):
        number_nights = data.get("number_nights")
        preferred_months = data.get("preferred_months")
        preferred_start_dow = data.get("preferred_start_dow")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if data["flexible_dates"]:
            if (
                number_nights == None
                or preferred_months == None
                or preferred_start_dow == None
            ):
                raise ValidationError(
                    "Missing required fields for flexible dates",
                )
        else:
            if start_date == None or end_date == None:
                raise ValidationError("Missing required fields for exact dates")
        if data.get("number_attendees") == None and (
            data.get("number_attendees_upper") == None
            or data.get("number_attendees_lower") == None
        ):
            raise ValidationError(
                "Missing number attendees, either range or exact number is required."
            )


class LodgingProposalRequestController(Resource):
    @use_args(LodgingProposalRequestPostSchema(), location="json")
    def post(self, post_data: dict):
        """Submit lodging proposal request form"""
        new_request = lodging_manager.create_lodging_proposal_request(
            email=post_data["email"],
            company_name=post_data["company_name"],
            flexible_dates=post_data["flexible_dates"],
            number_attendees=post_data.get("number_attendees"),
            number_attendees_upper=post_data.get("number_attendees_upper"),
            number_attendees_lower=post_data.get("number_attendees_lower"),
            meeting_spaces=post_data.get("meeting_spaces"),
            occupancy_types=post_data.get("occupancy_types"),
            number_nights=post_data.get("number_nights"),
            preferred_months=post_data.get("preferred_months"),
            preferred_start_dow=post_data.get("preferred_start_dow"),
            end_date=post_data.get("end_date"),
            start_date=post_data.get("start_date"),
        )
        if new_request:
            db.session.commit()
            return responses.success({"id": new_request.id}, 201)
        return responses.error("Unable to process request", 0, 500)


class RFPLiteResponseController(Resource):
    post_args = {
        "lodging_proposal_request_id": fields.Integer(
            required=True, data_key="lodgingProposalRequestId"
        ),
        "hotel": fields.String(required=True),
        "availability": fields.Boolean(required=True),
        "dates": fields.String(required=False),
    }

    @use_args(post_args, location="json")
    def post(self, post_args: dict):
        """
        Creates RFPLite response record.
        """
        lodging_manager.create_rfp_lite_response(
            post_args["lodging_proposal_request_id"],
            post_args["hotel"],
            post_args["availability"],
            post_args.get("dates"),
        )
        lodging_manager.commit_changes()
        return responses.success({"message": "Successfully recorded response"}, 201)
