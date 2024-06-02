from functools import wraps
import jwt
from flask import request, abort, g
import datetime
import logging


SECRET_KEY = "@V1um3JeWeTe!!"
OTP_SECRET = "0TP@V1um3JeWeTe!!"

def error_response(message, status_code):
    return {"error": True, "message": message}, status_code

def token_required(required_role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                
                return error_response("Unauthorized", 401)

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

                role = data.get("role", None)
                

                if required_role and required_role not in role:
                    return error_response("Unauthorized", 401)

                g.current_user = data

            except jwt.ExpiredSignatureError:
                return error_response("Token has expired", 401)
            except jwt.DecodeError as e:
                return error_response("Invalid Token", 401)
            except Exception as e:
                logging.error(f"Token verification error: {e}")
                return error_response("Something went wrong", 500)

            return f(*args, **kwargs)

        return decorated

    return decorator

def otp_required():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                
                return error_response("Unauthorized", 401)

            try:
                data = jwt.decode(token, OTP_SECRET, algorithms=["HS256"])

                email = data.get("email", None)
                

                if not email:
                    return error_response("Unauthorized", 401)

                g.current_user = data

            except jwt.ExpiredSignatureError:
                return error_response("Token has expired", 401)
            except jwt.DecodeError as e:
                return error_response("Invalid Token", 401)
            except Exception as e:
                logging.error(f"Token verification error: {e}")
                return error_response("Something went wrong", 500)

            return f(*args, **kwargs)

        return decorated

    return decorator

def generate_jwt_token(email, role):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    payload = {"email": email, "role": role, "exp": expiration_time}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_otp_token(email):
    expired_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    payload = {"email": email, "exp": expired_time}
    return jwt.encode(payload, OTP_SECRET, algorithm="HS256")
