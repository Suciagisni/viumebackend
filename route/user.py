from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.jwt import generate_jwt_token, token_required
from utils.auth import get_user
from schema.user_schema import ResponseUser
import logging

class User(MethodResource, Resource):
    # get user info by token header
    @doc(description='Get user info', tags=['User'], security=[{'BearerAuth': []}])
    @marshal_with(ResponseUser)
    @token_required(required_role="user")
    def get(self):
        try:
            current_user = getattr(g, 'current_user', {})
            user = get_user(current_user['email'])
            return {"error": False, "message": "Get user info success", "user": user}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get user info failed'}, 500
