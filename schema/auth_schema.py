from marshmallow import Schema, fields

class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)

class RegisterbyAdminSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    role = role = fields.List(fields.Str())

class UpdatebyAdminSchema(Schema):
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    role = role = fields.List(fields.Str())


class ResetSchema(Schema):
    email = fields.Email(required=True)
    currentpassword = fields.Str(required=True)
    newpassword = fields.Str(required=True)

