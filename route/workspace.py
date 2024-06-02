from flask import abort, current_app, g, request
from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from utils.jwt import generate_jwt_token, token_required
from utils.workspace import create_workspace, get_all_workspace, get_workspace_by_id, delete_workspace, get_workspace, update_workspace, get_all_workspace_collaborator, update_latest_imagecount
from schema.workspace_schema import WorkResponse, RegisterWorkspace, WorkResponseOne, UpdateWorkspace
import logging


class Workspace(MethodResource, Resource):
    # get all workspace  by token header
    @doc(description='Get Workspace info', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(WorkResponse)
    def get(self):
        try:
            current_user = getattr(g, 'current_user', {})
            workspace = get_all_workspace(current_user['email'])
            return {"error": False, "message": "Get workspace success", "workspace": workspace}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workspace failed'}, 500

    # create workspace
    @doc(description='Create Workspace', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @use_kwargs(RegisterWorkspace)
    def post(self, name, description, collaborator):
        try:
            current_user = getattr(g, 'current_user', {})
            result = create_workspace(
                email=current_user['email'], name=name, description=description, collaborator=collaborator)
            return result
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {"error": True, 'message': 'Registration failed'}, 500

       # update workspace by id
    @doc(description='Update Workspace by id', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @use_kwargs(UpdateWorkspace)
    def put(self, id, name, description, collaborator):
        try:
            current_user = getattr(g, 'current_user', {})
            result = update_workspace(
                id=id, email=current_user['email'], name=name, description=description, collaborator=collaborator)
            return result
        except Exception as e:
            logging.error(f"Update workspace info error: {e}")
            return {"error": True, 'message': 'Update workspace info failed'}, 500


class WorkspaceId(MethodResource, Resource):
    # get workspace by id
    @doc(description='Get Workspace by id', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(WorkResponseOne)
    def get(self, id):
        try:
            current_user = getattr(g, 'current_user', {})
            workspace = get_workspace(id, current_user['email'])
            if workspace:
                return {"error": False, "message": "Get workspace success", "workspace": workspace}, 200
            else:
                return {"error": True, "message": "Workspace not found"}, 404
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workspace failed'}, 403

    # delete workspace by id
    @doc(description='Delete Workspace by id', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(WorkResponseOne)
    def delete(self, id):
        try:
            current_user = getattr(g, 'current_user', {})
            result = delete_workspace(id, current_user['email'])
            return result
        except Exception as e:
            logging.error(f"Delete error: {e}")
            return {"error": True, 'message': 'Delete failed'}, 500


class SharedWorkspace(MethodResource, Resource):
    # get all workspace  by token header
    @doc(description='Get Workspace info', tags=['Workspace'], security=[{'BearerAuth': []}])
    @token_required(required_role="user")
    @marshal_with(WorkResponse)
    def get(self):
        try:
            current_user = getattr(g, 'current_user', {})
            workspace = get_all_workspace_collaborator(current_user['email'])
            return {"error": False, "message": "Get workspace success", "workspace": workspace}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workspace failed'}, 500


class temporaryAddImageAttribute(MethodResource, Resource):
    # get all workspace  by token header
    @token_required(required_role="admin")
    @doc(description='Get Workspace info', tags=['Admin'], security=[{'BearerAuth': []}])
    @marshal_with(WorkResponse)
    def get(self):
        try:

            workspace = update_latest_imagecount()
            return {"error": False, "message": "Get workspace success", "workspace": workspace}, 200
        except Exception as e:
            logging.error(f"Get user info error: {e}")
            return {"error": True, 'message': 'Get workspace failed'}, 500
