from hawk_models.base import ObjectSchema
from webargs import fields


class CompanyModelSchema(ObjectSchema):

    id = fields.Int(dump_only=True)
    name = fields.Str()


CompanyApiSchema = CompanyModelSchema()
