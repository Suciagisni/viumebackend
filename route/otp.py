from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.jwt import generate_otp_token
from utils.otp import generate_otp, verify_otp, send_otp_email
from utils.auth import get_user
from schema.otp_schema import ResponseOTP, ResponseVerifyOTP
import logging


class OTP(MethodResource, Resource):
    @doc(description='Get OTP info', tags=['OTP'])
    @use_kwargs({'email': fields.Email(required=True)})
    @marshal_with(ResponseOTP)
    def post(self, email):
        try:
            if get_user(email):
                return {"error": True, "message": "Email already exists"}, 409
            otp = generate_otp(email)
            send_otp_email(email, otp)
            return {"error": False, "message": "Get OTP success"}, 200
        except Exception as e:
            logging.error(f"Get OTP error: {e}")
            return {"error": True, 'message': 'Get OTP failed'}, 500

class VerifyOTP(MethodResource, Resource):
    @doc(description='Verify OTP info', tags=['OTP'])
    @use_kwargs({'email': fields.Email(required=True), 'otp': fields.String(required=True)})
    @marshal_with(ResponseVerifyOTP)
    def post(self, email, otp):
        try:
            result = verify_otp(email, otp)
            if result:
                return {"error": False, "message": "Verify OTP success", "token": generate_otp_token(email)}, 200
            else:
                return {"error": True, "message": "Verify OTP failed"}, 401
        except Exception as e:
            logging.error(f"Verify OTP error: {e}")
            return {"error": True, 'message': 'Verify OTP failed'}, 500
