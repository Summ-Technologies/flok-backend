from hawk_models.base import ObjectSchema
from webargs import fields


class UserModelSchema(ObjectSchema):

    id = fields.Int()
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


UserApiSchema = UserModelSchema()
