from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import create_model_with_response, validate_model, create_model_with_response
from app.models.goal import Goal
from datetime import datetime
from ..db import db
import os, requests

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# CREATE a goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_with_response(Goal, request_body)