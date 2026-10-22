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

# READ goals
@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)

    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals: 
        goals_response.append(goal.to_dict())

    return goals_response

# READ a goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

# UPDATE a goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE a goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
