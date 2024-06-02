from marshmallow import Schema, fields

class ResponseOTP(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)

class ResponseVerifyOTP(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    token = fields.Str()

