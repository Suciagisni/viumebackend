from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.jwt import generate_jwt_token, token_required
from utils.annotation import get_annotation, update_annotation, get_annotation_yolo, add_annotation
from schema.annotation_schema import UpdateAnnotationSchema
import logging

class Annotation(MethodResource, Resource):
    # get annotation by imageId
    @doc(description='Get Annotation info', tags=['Annotation'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    def get(self, imageId):
        try:
            annotation = get_annotation(imageId)
            return {"error": False, "message": "Get annotation success", "annotation": annotation}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get annotation failed'}, 500
    
    # add annotation by imageId
    @doc(description='Add Annotation info', tags=['Annotation'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @use_kwargs(UpdateAnnotationSchema)
    def post(self, imageId, listAnnotation):
        try:
            result = add_annotation(imageId, listAnnotation)
            return {"error": False, "message": "Add annotation success"}, 200
        except Exception as e:
            logging.error(f"Add annotation error: {e}")
            return {"error": True, 'message': 'Add annotation failed'}, 500

    # update annotation by imageId
    @doc(description='Update Annotation info', tags=['Annotation'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @use_kwargs(UpdateAnnotationSchema)
    def put(self, imageId, listAnnotation):
        try:
            result = update_annotation(imageId, listAnnotation)
            return {"error": False, "message": "Update annotation success"}, 200
        except Exception as e:
            logging.error(f"Update annotation error: {e}")
            return {"error": True, 'message': 'Update annotation failed'}, 500

class AnnotationYolo(MethodResource, Resource):
    # get annotation by imageId
    @doc(description='Get Annotation info', tags=['Annotation'], security=[{'BearerAuth': []}])
    @use_kwargs({'imageId':fields.String(required=True), 'image_width': fields.Int(required=True), 'image_height': fields.Int(required=True)})
    @token_required(required_role="user")
    def post(self, imageId, image_width, image_height):
        try:
            annotation = get_annotation_yolo(imageId, image_width, image_height)
            return {"error": False, "message": "Get annotation success", "annotation": annotation}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get annotation failed'}, 500