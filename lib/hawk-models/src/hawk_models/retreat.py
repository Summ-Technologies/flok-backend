from hawk_models.base import ObjectSchema
from hawk_models.lodging import LodgingPreferenceSchema
from webargs import fields


class RetreatSchema(ObjectSchema):

    id = fields.Int()
    name = fields.Str()
    selected_destination = fields.Function(
        lambda ret: DestinationSchema().dump(obj=ret.selected_destinations[0])
        if ret.selected_destinations
        else None
    )
    lodging_preference = fields.Function(
        lambda ret: LodgingPreferenceSchema().dump(obj=ret.lodging_preferences[0])
        if ret.lodging_preferences
        else None
    )

    lodging_proposals = fields.List(fields.Nested("LodgingProposalSchema"))
    employees = fields.List(fields.Nested("EmployeeSchema"))
    employees_flights = fields.List(fields.Nested("EmployeeFlightTrips"))
    # flights_slack_connect
    # itinerary
    # ground_transportation


class DestinationSchema(ObjectSchema):
    id = fields.Int()
    name = fields.Str()
    google_maps_id = fields.Str()
