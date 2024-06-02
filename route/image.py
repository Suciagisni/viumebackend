from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from werkzeug.datastructures import FileStorage, MultiDict
from werkzeug.utils import secure_filename
import os, pyvips
from schema.workbook_schema import WorkbookSchema, RegisterWorkbook, RegistResponse, RegistOneResponse, UpdateWorkbook
from PIL import Image as PilImage
from utils.workbook import create_workbook, get_workbook, get_all_workbook, get_all_workbook_by_workspace_id, delete_workbook, update_workbook, get_shared_image
from utils.jwt import generate_jwt_token, token_required
import numpy as np
import logging


PilImage.MAX_IMAGE_PIXELS = None


def allowed_file(filename):  
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tif', 'svs', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_tiles(image_path, output_dir):
    thumbnail_size = (256, 256)
    tile_size = 512

    pil_image = PilImage.open(image_path)
    pil_image.thumbnail(thumbnail_size)

    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')

    thumbnail_path = os.path.join(output_dir, "thumbnail.jpg")
    pil_image.save(thumbnail_path)

    vips_image = pyvips.Image.new_from_file(image_path)

    vips_image.dzsave(output_dir, layout="zoomify", suffix=".jpg[Q=95]", tile_size=tile_size)

    

class Image(MethodResource, Resource):
    @doc(description='Upload an image and process with pyvips', tags=['Image'], security=[{'BearerAuth': []}])
    @use_kwargs(RegisterWorkbook, location="form")
    @token_required(required_role="user")
    def post(self, **kwargs):
        try:

            form = request.form.to_dict()
           
            collab = request.form.getlist('collaborator')
            if collab:
                collaborator_emails = [email.strip() for email in collab[0].strip('[]').split(',')]
               
                form['collaborator'] = collaborator_emails
            else:
                form['collaborator'] = []

            app = current_app._get_current_object()
            current_user = getattr(g, 'current_user', {})
            form['email'] = current_user['email']
            files = request.files['file']  
            filename = secure_filename(files.filename)
            if files and allowed_file(filename):
                
                workbook = create_workbook(form)
                
                if workbook:
                    
                    # Save the uploaded image
                    uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], workbook['_id'])
                    files.save(uploaded_image_path)

                    # Create a directory for the tile folder
                    tile_folder_path = os.path.join(app.config['TILES_FOLDER'], workbook['_id'])
                    os.makedirs(tile_folder_path)

                    # Generate tiles using pyvips and save them in the tile folder
                    generate_tiles(uploaded_image_path, tile_folder_path)

                    return {"error": False, 'message': "Berhasil Upload Files", "imageId": workbook['_id']}, 200
                else:
                    return {"error": False, 'message': "Gagal Upload Files"}, 200

            return {"error": True, 'message': "Invalid File"}, 404
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500
    
    @doc(description='Get all workbook  by token header', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(RegistResponse)
    def get(self):
        try:
            current_user = getattr(g, 'current_user', {})
            workbook = get_all_workbook(current_user['email'])
            return {"error": False, "message": "Get workbook success", "workbook": workbook}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workbook failed'}, 500

    # edit workbook
    @doc(description='Update Workbook', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @use_kwargs(UpdateWorkbook)
    def put(self, id, name, collaborator, isPublic, zoomLevel=1):
        try:
            current_user = getattr(g, 'current_user', {})
            result = update_workbook(id=id, email=current_user['email'], name=name, collaborator=collaborator, isPublic=isPublic, zoomLevel=zoomLevel)
            return result
        except Exception as e:
            logging.error(f"Update workbook info error: {e}")
            return {"error": True, 'message': 'Update workbook info failed'}, 500
    


class ImageId(MethodResource, Resource):
    # get workbook by id and email
    @doc(description='Get Workbook by id', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(RegistOneResponse)
    def get(self, id):
        try:
            current_user = getattr(g, 'current_user', {})
        
            workbook = get_workbook(id, current_user['email'])
            if workbook:
                return {"error": False, "message": "Get workbook success", "workbook": workbook}, 200
            else:
                return {"error": True, "message": "workbook not found"}, 404
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workbook failed'}, 403

        # delete workbook by id
    @doc(description='Delete Workbook by id', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(RegistOneResponse)
    def delete(self, id):
        try:
            current_user = getattr(g, 'current_user', {})
            workbook = get_workbook(id, current_user['email'])
            if workbook:
                result = delete_workbook(id)
            return {"error": False, "message": "Delete workbook success"}, 200
        except Exception as e:
            logging.error(f"Delete error: {e}")
            return {"error": True, 'message': 'Delete failed'}, 500

class WorkbookId(MethodResource, Resource):
    # get workbook by workspace id
    @doc(description='Get Workbook by workspace id', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(RegistResponse)
    def get(self, id):
        try:
            current_user = getattr(g, 'current_user', {})
            workbook = get_all_workbook_by_workspace_id(id)
            if workbook:
                return {"error": False, "message": "Get workbook success", "workbook": workbook}, 200
            else:
                return {"error": True, "message": "workbook not found"}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workbook failed'}, 403


class SharedImage(MethodResource, Resource):
    # get workbook by email from get_shared_image
    @doc(description='Get Shared Image', tags=['Image'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(RegistResponse)
    def get(self):
        try:
            current_user = getattr(g, 'current_user', {})
            workbook = get_shared_image(current_user['email'])
            if workbook:
                return {"error": False, "message": "Get workbook success", "workbook": workbook}, 200
            else:
                return {"error": True, "message": "workbook not found"}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workbook failed'}, 403