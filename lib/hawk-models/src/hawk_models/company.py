from hawk_models.base import ObjectSchema
from webargs import fields


class CompanySchema(ObjectSchema):

    id = fields.Int(dump_only=True)
    name = fields.Str()
    employees = fields.List(fields.Nested("EmployeeSchema"))
    retreats = fields.List(fields.Nested("RetreatSchema"))
