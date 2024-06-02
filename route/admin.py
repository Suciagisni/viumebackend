from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.jwt import generate_jwt_token, token_required
from utils.auth import get_all_users, delete_user, get_user, register_by_admin, update_by_admin
from schema.user_schema import ResponseUser
from schema.auth_schema import RegisterbyAdminSchema, UpdatebyAdminSchema
from utils.workbook import delete_folders_if_id_not_found
import logging


class ListAllUsers(MethodResource, Resource):
    # get all users
    @doc(description='Get all users info', tags=['Admin'], security=[{'BearerAuth': []}])
    @token_required(required_role="admin")
    def get(self):
        try:
            users = get_all_users()
            return {"error": False, "message": "Get all users success", "users": users}, 200
        except Exception as e:
            logging.error(f"Get all users error: {e}")
            return {"error": True, 'message': 'Get all users failed'}, 500


class UsersWithId(MethodResource, Resource):
    # get user by email
    @doc(description='Get user info by email', tags=['Admin'], security=[{'BearerAuth': []}])
    @marshal_with(ResponseUser)
    @token_required(required_role="admin")
    def get(self, email):
        try:
            user = get_user(email)
            if user:
                return {"error": False, "message": "Get user info success", "user": user}, 200
            else:
                return {"error": True, "message": "User not found"}, 404
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get user info failed'}, 500
    
    # delete user by email
    @doc(description='Delete user by email', tags=['Admin'], security=[{'BearerAuth': []}])
    @marshal_with(ResponseUser)
    @token_required(required_role="admin")
    def delete(self, email):
        try:
            user = get_user(email)
            if user:
                result = delete_user(email)
                return {"error": False, "message": "Delete user success"}, 200
            else:
                return {"error": True, "message": "User not found"}, 404
        except Exception as e:
            logging.error(f"Delete error: {e}")
            return {"error": True, 'message': 'Delete failed'}, 500


class RegisterbyAdmin(MethodResource, Resource):
    @doc(description='Register', tags=['Admin'], security=[{'BearerAuth': []}])
    @use_kwargs(RegisterbyAdminSchema)
    @token_required(required_role="admin")
    def post(self, email, password, first_name, last_name, username, role):
        try:
            result = register_by_admin(email=email, password=password, first_name=first_name, last_name=last_name, username=username, role=role)
            return result
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {"error": True, 'message': 'Registration failed'}, 500

class UpdatebyAdmin(MethodResource, Resource):
    @doc(description='Update user info', tags=['Admin'], security=[{'BearerAuth': []}])
    @use_kwargs(UpdatebyAdminSchema)
    @token_required(required_role="admin")
    def put(self, email, first_name, last_name, username, role):
        try:
            result = update_by_admin(email=email, first_name=first_name, last_name=last_name, username=username, role=role)
            return result
        except Exception as e:
            logging.error(f"Update user info error: {e}")
            return {"error": True, 'message': 'Update user info failed'}, 500

class ClearFile(MethodResource, Resource):
    @doc(description='Clear file', tags=['Admin'], security=[{'BearerAuth': []}])
    @token_required(required_role="admin")
    def delete(self):
        try:
            result = delete_folders_if_id_not_found()
            return result
        except Exception as e:
            logging.error(f"Clear file error: {e}")
            return {"error": True, 'message': 'Clear file failed'}, 500