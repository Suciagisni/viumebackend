from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.auth import login, register, change_password
from utils.jwt import generate_jwt_token, token_required, otp_required
from schema.auth_schema import AuthSchema, RegisterSchema, ResetSchema
import logging


class Login(MethodResource, Resource):
    @doc(description='Login', tags=['Auth'])
    @use_kwargs(AuthSchema)
    def post(self, email, password):
        try:
            user = login(email, password)
            if user:
                token = generate_jwt_token(email, user['role'])
                return {"error": False, "message": "Login success", "user": user, "token": token}, 200
            else:
                return {"error": True, "message": "Login failed"}, 401
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500


class ChangePass(MethodResource, Resource):
    @doc(description='Change Password', tags=['Auth'])
    @use_kwargs(ResetSchema)
    def post(self, email, currentpassword, newpassword):
        try:
            user = login(email, currentpassword)
            if user:
                reset = change_password(email, currentpassword, newpassword)
                if reset:
                    return {"error": False, "message": "Change Password Success"}, 200
                else:
                    return {"error": True, "message": "Change Password Failed"}, 401
            else:
                return {"error": True, "message": "Invalid Account"}, 401
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500


class Register(MethodResource, Resource):
    @doc(description='Register', tags=['Auth'],  security=[{'BearerAuth': []}])
    @use_kwargs(RegisterSchema)
    @otp_required()
    def post(self, email, password, first_name, last_name, username):
        try:
            current_user = getattr(g, 'current_user', {})
            if current_user['email'] != email:
                return {"error": True, "message": "Invalid OTP"}, 401
            result = register(email=email, password=password,
                              first_name=first_name, last_name=last_name, username=username)
            return result
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {"error": True, 'message': 'Registration failed'}, 500
