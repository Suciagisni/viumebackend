from marshmallow import Schema, fields

class WorkspaceSchema(Schema):
    _id = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    collaborator = fields.List(fields.Str())
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    isPublic = fields.Boolean(required=True)
    image_count = fields.Int(required=True)

class RegisterWorkspace(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    collaborator = fields.List(fields.Str())

class UpdateWorkspace(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    collaborator = fields.List(fields.Str())

class WorkResponse(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    workspace = fields.Nested(WorkspaceSchema, many=True)

class WorkResponseOne(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    workspace = fields.Nested(WorkspaceSchema)