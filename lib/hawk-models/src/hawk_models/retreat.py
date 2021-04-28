from __future__ import annotations

from marshmallow.schema import Schema
from webargs import fields


class RetreatEmployeeLocationItemModelSchema(Schema):

    id = fields.Int(dump_only=True)
    submission_id = fields.Int(dump_only=True)
    employee_count = fields.Int(required=True)
    google_place_id = fields.String(required=True)
    main_text = fields.String(required=True)
    secondary_text = fields.String(required=True)


RetreatEmployeeLocationItemApiSchema = RetreatEmployeeLocationItemModelSchema()


class RetreatEmployeeLocationSubmissionSchema(Schema):

    id = fields.Int(dump_only=True)
    retreat_id = fields.Int(dump_only=True)
    location_items = fields.Nested("RetreatEmployeeLocationItemModelSchema", many=True)
    created_at = fields.AwareDateTime(dump_only=True)
    extra_info = fields.String()


RetreatEmployeeLocationSubmissionApiSchema = RetreatEmployeeLocationSubmissionSchema()


class RetreatProposalModelSchema(Schema):

    id = fields.Int(dump_only=True)
    retreat_id = fields.Int(dump_only=True)
    created_at = fields.AwareDateTime(dump_only=True)

    image_url = fields.URL(required=True)
    title = fields.String(required=True)
    body = fields.String()
    flight_time_avg = fields.Float(required=True)

    lodging_cost = fields.Integer(required=True)
    flights_cost = fields.Integer(required=True)
    other_cost = fields.Integer(required=True)

    extra_info = fields.String()


RetreatProposalApiSchema = RetreatProposalModelSchema()


class RetreatModelSchema(Schema):

    id = fields.Int(dump_only=True)
    company_id = fields.Int(dump_only=True)
    name = fields.Str()
    employee_location_submission = fields.Function(
        serialize=lambda obj: RetreatEmployeeLocationSubmissionApiSchema.dump(
            obj=obj.employee_location_submissions[0]
        )
        if obj.employee_location_submissions
        else None
    )
    proposals = fields.Function(
        serialize=lambda obj: RetreatProposalApiSchema.dump(
            obj=obj.proposals, many=True
        )
    )
    selected_proposal_id = fields.Int()
    num_employees = fields.Int(required=True)
    num_nights = fields.Int(required=True)


RetreatApiSchema = RetreatModelSchema()
