from marshmallow import Schema, fields

class UpdateAnnotationSchema(Schema):
    imageId = fields.String(required=True)
    listAnnotation = fields.List(fields.Dict(), required=True)
