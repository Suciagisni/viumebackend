from marshmallow import Schema, fields



class UserSchema(Schema):
    _id = fields.Str(required=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    is_active = fields.Boolean(required=True)
    role = fields.List(fields.Str(), required=True)


class ResponseUser(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    user = fields.Nested(UserSchema, required=False)






