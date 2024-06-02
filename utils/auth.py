from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw
import datetime
from email_validator import validate_email, EmailNotValidError
from config.db import db

users = db['users']

MAX_USERNAME_LENGTH = 10

def login(email, password):
    user = users.find_one({'email': email})
    if user and checkpw(password.encode('utf-8'), user['password']):
        sanitized_user = {
            "_id": str(user["_id"]),
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "username": user["username"],
            "created_at": user["created_at"].isoformat(),
            "updated_at": user["updated_at"].isoformat(),
            "is_active": user["is_active"],
            "role": user["role"],
        }
        return sanitized_user
    else:
        return None

def register(**kwargs):
    try:
        valid_email = validate_email(kwargs['email']).email
    except EmailNotValidError as e:
        return {"error": True, "message": "Invalid email format"}, 400

    user = users.find_one({'email': kwargs['email'].lower()})
    if user:
        return {"error": True, "message": "Email already in use"}, 400

    hashed_password = hashpw(kwargs['password'].encode('utf-8'), gensalt())
    kwargs['email'] = kwargs['email'].lower()
    kwargs['password'] = hashed_password
    kwargs['created_at'] = datetime.datetime.now()
    kwargs['updated_at'] = datetime.datetime.now()
    kwargs['is_active'] = True
    kwargs['role'] = ['user']

    if len(kwargs['username']) > MAX_USERNAME_LENGTH:
        return {"error": True, "message": f"Username is too long (maximum {MAX_USERNAME_LENGTH} characters)"}, 400


    result = users.insert_one(kwargs)
    if result.inserted_id:
        return {"error": False, "message": "Registration successful", "user_id": str(result.inserted_id)}, 200
    else:
        return {"error": True, "message": "Registration failed"}, 500



def change_password(email, current_password, new_password):
    user = users.find_one({'email': email})
    if user and checkpw(current_password.encode('utf-8'), user['password']):
        new_password_hashed = hashpw(new_password.encode('utf-8'), gensalt())
        users.update_one({'email': email}, {'$set': {'password': new_password_hashed}})
        return True
    else:
        return False


def get_user(email):
    user = users.find_one({'email': email.lower()})
    if user:
        sanitized_user = {
            "_id": str(user["_id"]),
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "username": user["username"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
            "is_active": user["is_active"],
            "role": user["role"],
        }
        return sanitized_user
    else:
        return None

def delete_user(email):
    users.delete_one({'email': email.lower()})
    return True

def get_all_users():
    result = users.find()
    if result:
        sanitized_result = []
        for user in result:
            sanitized_user = {
                "_id": str(user["_id"]),
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "username": user["username"],
                "created_at": user["created_at"].isoformat(),
                "updated_at": user["updated_at"].isoformat(),
                "is_active": user["is_active"],
                "role": user["role"],
            }
            sanitized_result.append(sanitized_user)
        return sanitized_result
    else:
        return None


def register_by_admin(**kwargs):
    try:
        valid_email = validate_email(kwargs['email']).email
    except EmailNotValidError as e:
        return {"error": True, "message": "Invalid email format"}, 400

    user = users.find_one({'email': kwargs['email'].lower()})
    if user:
        return {"error": True, "message": "Email already in use"}, 400

    hashed_password = hashpw(kwargs['password'].encode('utf-8'), gensalt())
    kwargs['email'] = kwargs['email'].lower()
    kwargs['password'] = hashed_password
    kwargs['created_at'] = datetime.datetime.now()
    kwargs['updated_at'] = datetime.datetime.now()
    kwargs['is_active'] = True
    kwargs['role'] = kwargs['role']

    if len(kwargs['username']) > MAX_USERNAME_LENGTH:
        return {"error": True, "message": f"Username is too long (maximum {MAX_USERNAME_LENGTH} characters)"}, 400


    result = users.insert_one(kwargs)
    if result.inserted_id:
        return {"error": False, "message": "Registration successful", "user_id": str(result.inserted_id)}, 200
    else:
        return {"error": True, "message": "Registration failed"}, 500

def update_by_admin(email, first_name, last_name, username, role):
    try:
        valid_email = validate_email(email).email
    except EmailNotValidError as e:
        return {"error": True, "message": "Invalid email format"}, 400
    
    user = users.find_one({'email': email.lower()})
    if user:
        users.update_one({'email': email.lower()}, {'$set': {'first_name': first_name, 'last_name': last_name, 'username': username, 'role': role}})
        return {"error": False, "message": "Update user success"}, 200
    else:
        return {"error": True, "message": "User not found"}, 404