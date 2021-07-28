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
    number_attendees = fields.Integer(min=0, data_key="numberAttendees")
    number_attendees_range = fields.Tuple(
        (fields.Integer(min=0), fields.Integer(min=0)), data_key="numberAttendeesRange"
    )
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
        if (
            data.get("number_attendees") == None
            and data.get("number_attendees_range") == None
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
            flexible_dates=post_data["flexible_dates"],
            number_attendees=post_data.get("number_attendees"),
            number_attendees_range=post_data.get("number_attendees_range"),
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
            return responses.success({"message": "Successfully created"}, 201)
        return responses.error("Unable to process request", 0, 500)
