from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from route.image import Image, ImageId, WorkbookId, SharedImage
import os
from route.tiles import TileImage, XMLInfo, Thumbnail
from route.auth import Login, Register, ChangePass
from route.user import User
from route.workspace import Workspace, WorkspaceId, SharedWorkspace, temporaryAddImageAttribute
from route.annotation import Annotation, AnnotationYolo
from route.admin import ListAllUsers, UsersWithId, RegisterbyAdmin, UpdatebyAdmin, ClearFile
from route.otp import OTP, VerifyOTP

app = Flask(__name__)    
api = Api(app)

CORS(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='ViuMe',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0',
        securityDefinitions={ 
            'BearerAuth': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Enter your Bearer token in the format: Bearer <token>'
            }
        }
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  
    'APISPEC_SWAGGER_UI_URL': '/docs/'  
})


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Move up one level to the viume directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'image', 'uploads')
TILES_FOLDER = os.path.join(BASE_DIR, 'image', 'tiles')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TILES_FOLDER'] = TILES_FOLDER

docs = FlaskApiSpec(app)




api.add_resource(Image, '/image')
docs.register(Image)

api.add_resource(ImageId, '/image/<string:id>')
docs.register(ImageId)

api.add_resource(SharedImage, '/image/shared')
docs.register(SharedImage)

api.add_resource(WorkbookId, '/workbook/<string:id>')
docs.register(WorkbookId)

api.add_resource(TileImage, '/tiles/<string:image_name>/<string:pyramid_folder>/<string:col_row>')
docs.register(TileImage)

api.add_resource(XMLInfo, '/xmltiles/<string:image_name>')
docs.register(XMLInfo)

api.add_resource(Login, '/login')
docs.register(Login)

api.add_resource(ChangePass, '/resetpass')
docs.register(ChangePass)


api.add_resource(Register, '/register')
docs.register(Register)

api.add_resource(User, '/user')
docs.register(User)

api.add_resource(Workspace, '/workspace')
docs.register(Workspace)

api.add_resource(WorkspaceId, '/workspace/<string:id>')
docs.register(WorkspaceId)

api.add_resource(SharedWorkspace, '/workspace/shared')
docs.register(SharedWorkspace)

api.add_resource(Thumbnail, '/thumbnail/<string:image_name>')
docs.register(Thumbnail)

api.add_resource(Annotation, '/annotation/<string:imageId>')
docs.register(Annotation)

api.add_resource(AnnotationYolo, '/annotation/yolo')
docs.register(AnnotationYolo)

api.add_resource(ListAllUsers, '/admin/users')
docs.register(ListAllUsers)

api.add_resource(UsersWithId, '/admin/users/<string:email>')
docs.register(UsersWithId)

api.add_resource(RegisterbyAdmin, '/admin/users')
docs.register(RegisterbyAdmin)

api.add_resource(UpdatebyAdmin, '/admin/users/<string:email>')
docs.register(UpdatebyAdmin)

api.add_resource(ClearFile, '/admin/clear')
docs.register(ClearFile)

api.add_resource(temporaryAddImageAttribute, '/admin/syncImage')
docs.register(temporaryAddImageAttribute)

api.add_resource(OTP, '/otp')
docs.register(OTP)

api.add_resource(VerifyOTP, '/otp/verify')  
docs.register(VerifyOTP)




if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
