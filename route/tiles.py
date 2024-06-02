from flask import abort, current_app, g, request, send_from_directory, make_response
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os, pyvips
from xml.etree import ElementTree as ET
from utils.jwt import generate_jwt_token, token_required

class TileImage(MethodResource, Resource):
    @doc(description='get images', tags=['Image'])
    def get(self, image_name, pyramid_folder, col_row):
        try:
            app = current_app._get_current_object()

            tile_path = os.path.join(app.config['TILES_FOLDER'], image_name, pyramid_folder, f"{col_row}")
           
            if os.path.exists(tile_path):
                response = make_response(send_from_directory(os.path.dirname(tile_path), os.path.basename(tile_path)))


                response.headers['Cache-Control'] = 'max-age=31536000, immutable'

                return response
                # return send_from_directory(os.path.dirname(tile_path), os.path.basename(tile_path))
            else:
                return {"error": True, "message": "Tile image not found"}, 404
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500

class XMLInfo(MethodResource, Resource):
    @doc(description='get xml info', tags=['Image'])
    @token_required(required_role="user")
    def get(self, image_name):
        try:
            app = current_app._get_current_object()

            # Construct the path to the ImageProperties.xml file
            xml_path = os.path.join(app.config['TILES_FOLDER'], image_name, 'ImageProperties.xml')

            # Parse the XML file to extract width and height
            tree = ET.parse(xml_path)
            root = tree.getroot()
            width = int(root.attrib['WIDTH'])
            height = int(root.attrib['HEIGHT'])
            tile_size = int(root.attrib['TILESIZE'])

            return {"width": width, "height": height, "tile_size": tile_size}, 200
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500

class Thumbnail(MethodResource, Resource):
    @doc(description='get images', tags=['Image'])
    def get(self, image_name):
        try:
            app = current_app._get_current_object()

            # Construct the path to the tile image based on the requested parameters
            tile_path = os.path.join(app.config['TILES_FOLDER'], image_name, "thumbnail.jpg")

            # Check if the tile image exists

            if os.path.exists(tile_path):
                return send_from_directory(os.path.dirname(tile_path), os.path.basename(tile_path))
            else:
                return {"error": True, "message": "Tile image not found"}, 404
        except Exception as e:
            return {"error": True, 'message': str(e)}, 500