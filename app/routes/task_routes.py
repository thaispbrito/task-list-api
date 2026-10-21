from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import validate_model, validate_data
from app.models.task import Task
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# CREATE a task
@bp.post("")
def create_task():
    request_body = request.get_json()
    validate_data(request_body)

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

# READ tasks
@bp.get("")
def get_all_tasks():

    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_dict())

    return tasks_response

# READ a task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

# UPDATE a task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE a task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")