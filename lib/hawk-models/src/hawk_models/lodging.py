from hawk_db.retreat import Dates, MeetingSpace, RoomingPreferences
from hawk_models.base import ObjectSchema
from serde.json import from_json
from webargs import fields


class LodgingPartnerSchema(ObjectSchema):
    id = fields.Int()
    name = fields.Str()
    contact = fields.Str()
    description = fields.Str()
    image_url = fields.Url()


class LodgingProposalSchema(ObjectSchema):
    id = fields.Int()
    destination_id = fields.Int()
    lodging_partner = fields.Function()
    proposal_url = fields.Url()


class LodgingPreferenceSchema(ObjectSchema):
    id = fields.Int()
    retreat_id = fields.Int()
    num_employees = fields.Int()
    dates = fields.Function(deserialize=lambda lp: from_json(Dates, lp.dates))
    meeting_space = fields.Function(
        deserialize=lambda lp: from_json(MeetingSpace, lp.meeting_space)
    )
    rooming_preferences = fields.Function(
        deserialize=lambda lp: from_json(RoomingPreferences, lp.rooming_preferences)
    )
    created_at = fields.AwareDateTime()
