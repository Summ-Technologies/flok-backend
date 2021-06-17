from hawk_models.base import ObjectSchema
from webargs import fields


class EmployeeSchema(ObjectSchema):
    id = fields.Int()
    company_id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    location = fields.Str()
    preferred_airport = fields.Str()
