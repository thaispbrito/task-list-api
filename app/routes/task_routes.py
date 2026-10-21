from flask import Blueprint, abort, make_response, request
from app.models.task import Task
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201