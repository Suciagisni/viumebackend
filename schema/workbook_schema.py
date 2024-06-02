from marshmallow import Schema, fields


class WorkbookSchema(Schema):
    _id = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    workspace_id = fields.Str(required=True)
    collaborator = fields.List(fields.Str())
    isPublic = fields.Boolean(required=True)
    file_status = fields.Boolean(required=True)
    ml_status = fields.Boolean(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    zoomLevel = fields.Int(required=False)


class RegisterWorkbook(Schema):
    file = fields.Raw(type='file')
    name = fields.Str(required=True)
    workspace_id = fields.Str(required=True)
    collaborator = fields.List(fields.Str())
    isPublic = fields.Boolean(required=True)
    zoomLevel = fields.Int(required=False)
    
class RegistResponse(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    workbook = fields.Nested(WorkbookSchema, many=True)

class RegistOneResponse(Schema):
    error = fields.Boolean(required=True)
    message = fields.Str(required=True)
    workbook = fields.Nested(WorkbookSchema)

class UpdateWorkbook(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    collaborator = fields.List(fields.Str())
    isPublic = fields.Boolean(required=True)
    zoomLevel = fields.Int(required=False)