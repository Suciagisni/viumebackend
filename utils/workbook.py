from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw
import datetime
from email_validator import validate_email, EmailNotValidError
from config.db import db
from bson import ObjectId
import os
import shutil
from flask import current_app

workbook = db['workbook']
workspace = db['workspace']




# create workbook with name, email, collaborator
def create_workbook(data):
    data['created_at'] = datetime.datetime.now()
    data['updated_at'] = datetime.datetime.now()
    data['file_status'] = False
    data['ml_status'] = False

    result = workbook.insert_one(data)
    if result.inserted_id:

        # update image count in workspace
        workspace_id = ObjectId(data['workspace_id'])
        workspace.update_one({'_id': workspace_id}, {'$inc': {'image_count': 1}})
        
        sanitized_workbook = {
            "_id": str(result.inserted_id),
            "email": data["email"],
            "name": data["name"],
            "workspace_id": data["workspace_id"],
            "collaborator": data["collaborator"],
            "file_status": data["file_status"],
            "ml_status": data["ml_status"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "isPublic": data["isPublic"],
            "zoomLevel": data.get("zoomLevel", 1),
        }
        return sanitized_workbook
    else:
        return None

# get all workbook with email and if email in collaborator list
def get_all_workbook(email):
    result = workbook.find({'$or': [{'email': email}, {'collaborator': email}]})
    if result:
        sanitized_workbook = []
        for item in result:
            sanitized_workbook.append({
                "_id": str(item["_id"]),
                "email": item["email"],
                "name": item["name"],
                "workspace_id": item["workspace_id"],
                "collaborator": item["collaborator"],
                "file_status": item["file_status"],
                "ml_status": item["ml_status"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "zoomLevel": item.get("zoomLevel", 1),
                "isPublic": item.get("isPublic", False),
            })
        return sanitized_workbook
    else:
        return None

# get all workbook with workspace_id
def get_all_workbook_by_workspace_id(workspace_id):
    result = workbook.find({'workspace_id': workspace_id})
    if result:
        sanitized_workbook = []
        for item in result:
            sanitized_workbook.append({
                "_id": str(item["_id"]),
                "email": item["email"],
                "name": item["name"],
                "workspace_id": item["workspace_id"],
                "collaborator": item["collaborator"],
                "file_status": item["file_status"],
                "ml_status": item["ml_status"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "zoomLevel": item.get("zoomLevel", 1),
                "isPublic": item["isPublic"],
            })
        return sanitized_workbook
    else:
        return None

def get_workbook(id, email):
    workbook_id = ObjectId(id)
    
    # check workbook only with id
    dataworkbook = workbook.find_one({'_id': workbook_id})
    if dataworkbook:
        if dataworkbook['email'] == email:
            return dataworkbook
        elif email in dataworkbook['collaborator']:
            return dataworkbook
        
        workspace_id = ObjectId(dataworkbook['workspace_id'])
        dataworkspace = workspace.find_one({'_id': workspace_id})
        if dataworkspace and dataworkspace['email'] == email:
            return dataworkbook
        elif dataworkspace and email in dataworkspace['collaborator']:
            return dataworkbook
        else:
            return None
    else:
        return None


   


# delete workbook with id and email
def delete_workbook(id):
    workbook_id = ObjectId(id)
    workbook_info = workbook.find_one({'_id': workbook_id})
    result = workbook.delete_one({'_id': workbook_id})
    if result.deleted_count:

        workspace_id = ObjectId(workbook_info['workspace_id'])
        workspace.update_one({'_id': workspace_id}, {'$inc': {'image_count': -1}})

        app = current_app._get_current_object()
        folder_path = os.path.join(app.config['TILES_FOLDER'], str(id))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        if os.path.exists(file_path):

            os.remove(file_path) 

        return True
    else:
        return False
    
# update workbook with id and email
def update_workbook(id, email, name, collaborator, isPublic, zoomLevel):
    workbook_id = ObjectId(id)
    result = workbook.update_one({'_id': workbook_id, 'email': email}, {'$set': {'name': name, 'collaborator': collaborator, 'isPublic': isPublic, 'zoomLevel': zoomLevel, 'updated_at': datetime.datetime.now()}})
    if result.modified_count:
        return {"error": False, "message": "Update workbook success"}, 200
    else:
        return {"error": True, "message": "Update workbook failed"}, 500

# get all image if email in collaborator list
def get_shared_image(email):
    result = workbook.find({'collaborator': email})
    if result:
        sanitized_workbook = []
        for item in result:
            sanitized_workbook.append({
                "_id": str(item["_id"]),
                "email": item["email"],
                "name": item["name"],
                "workspace_id": item["workspace_id"],
                "collaborator": item["collaborator"],
                "file_status": item["file_status"],
                "ml_status": item["ml_status"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "zoomLevel": item.get("zoomLevel", 1),
                "isPublic": item.get("isPublic", False),
            })
        return sanitized_workbook
    else:
        return None
    

def delete_folders_if_id_not_found():
    workbook_ids = [str(item["_id"]) for item in workbook.find({})]

    upload_dirs = os.listdir(current_app.config['UPLOAD_FOLDER'])

    for dir_name in upload_dirs:
        if dir_name not in workbook_ids:
            print(dir_name)
            folder_path = os.path.join(current_app.config['TILES_FOLDER'], dir_name)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], dir_name)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return {"error": False, "message": "Clear file success"}, 200