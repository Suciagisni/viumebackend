from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw
import datetime
from email_validator import validate_email, EmailNotValidError
from config.db import db
from bson import ObjectId
from utils.workbook import delete_workbook

workspace = db['workspace']
workbook = db['workbook']

# create workspace (folder) with email, name, description, list of email (collaborator)
def create_workspace(**kwargs):
    kwargs['created_at'] = datetime.datetime.now()
    kwargs['updated_at'] = datetime.datetime.now()
    kwargs['isPublic'] = False
    kwargs['image_count'] = 0

    result = workspace.insert_one(kwargs)
    if result.inserted_id:
        return {"error": False, "message": "Registration successful", "id": str(result.inserted_id)}, 200
    else:
        return {"error": True, "message": "Registration failed"}, 500


# get all worspace with email 
def get_all_workspace(email):
    result = workspace.find({'email': email})
    if result:
        sanitized_workspace = []
        for item in result:
            sanitized_workspace.append({
                "_id": str(item["_id"]),
                "email": item["email"],
                "name": item["name"],
                "description": item["description"],
                "collaborator": item["collaborator"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "isPublic": item["isPublic"],
                "image_count": item["image_count"],
            })
        return sanitized_workspace
    else:
        return None

# get all workspace with email if email in collaborator list
def get_all_workspace_collaborator(email):
    result = workspace.find({'collaborator': email})
    if result:
        sanitized_workspace = []
        for item in result:
            sanitized_workspace.append({
                "_id": str(item["_id"]),
                "email": item["email"],
                "name": item["name"],
                "description": item["description"],
                "collaborator": item["collaborator"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "isPublic": item["isPublic"],
                "image_count": item["image_count"],
            })
        return sanitized_workspace
    else:
        return None

def get_workspace_by_id(id):
    result = workspace.find_one({'_id': id})
    if result:
        return result
    else:
        return None

# get workspace with id and email if email in collaborator list or email is owner or workspace is public
def get_workspace(id, email):
    workspace_id = ObjectId(id)
    result = workspace.find_one({'$or': [{'_id': workspace_id, 'email': email}, {'_id': workspace_id, 'collaborator': email}, {'_id': workspace_id, 'isPublic': True}]})
    if result:
        return result
    else:
        return None


# delete workspace with id and email
def delete_workspace(id, email):
    workspace_id = ObjectId(id)
    result = workspace.delete_one({'_id': workspace_id, 'email': email})

    # delete all workbook that belong to workspace
    listWorkbook = workbook.find({'workspace_id': id})
    for item in listWorkbook:
        delete_workbook(item['_id'])


    if result.deleted_count:
        return {"error": False, "message": "Delete workspace success"}, 200
    else:
        return {"error": True, "message": "Delete workspace failed"}, 491


# update workspace with id and email
def update_workspace(id, email, name, collaborator, description):
    workspace_id = ObjectId(id)
    result = workspace.update_one({'_id': workspace_id, 'email': email}, {'$set': {'name': name, 'collaborator': collaborator, 'description': description, 'updated_at': datetime.datetime.now()}})
    if result.modified_count:
        return {"error": False, "message": "Update workspace success"}, 200
    else:
        return {"error": True, "message": "Update workspace failed"}, 500
    


# update image count in all workspace from all workbook
def update_latest_imagecount():
    list_workspace = workspace.find({})
    for item in list_workspace:
        workspace_id = item['_id']
        image_count = workbook.count_documents({'workspace_id': str(workspace_id)})
        workspace.update_one({'_id': workspace_id}, {'$set': {'image_count': image_count}})
