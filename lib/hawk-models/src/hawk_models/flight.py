from hawk_models.base import ObjectSchema
from webargs import fields


class FlightLegSchema(ObjectSchema):

    id = fields.Int()

    flight_trip_id = fields.Int()
    flight_number = fields.Str()
    from_airport = fields.Str()
    to_airport = fields.Str()
    departure_at = fields.AwareDateTime()
    arrival_at = fields.AwareDateTime()
    flight_time = fields.Int()


class FlightTripSchema(ObjectSchema):
    id = fields.Int()
    travel_time = fields.Int()
    flight_legs = fields.List(fields.Nested("FlightLegSchema"))


class EmployeeFlightTripSchema(ObjectSchema):
    arrival_flight_trip = fields.Nested("FlightTripSchema")
    departure_flight_trip = fields.Nested("FlightTripSchema")
    status = fields.Str()
    employee_id = fields.Int()
    retreat_id = fields.Int()
    est_cost = fields.Int()
    final_cost = fields.Int()
    url = fields.Str()
