from flask import (
  Blueprint,
  flash,
  g,
  redirect,
  render_template,
  request,
  url_for
)
from werkzeug.exceptions import abort

from flask import Blueprint, jsonify, g, request, abort, redirect, url_for
import services.db_handler as db_handler
import controllers.auth as auth

bp = Blueprint('todo', __name__)
db_handler = db_handler.DBHandler("todo")

@bp.route('/', methods=['GET'])
@auth.login_required
def index():
    todos = db_handler.get_todo_by_user_id(g.user["_id"])
    return jsonify(todos), 200

@bp.route('/create', methods=['POST'])
@auth.login_required
def create():
    name = request.json.get('name')
    description = request.json.get('description')
    error = None

    if not description:
        error = 'Description required'

    if error is not None:
        return jsonify({"error": error}), 400
    else:
        db_handler.add_todo(name, description, False, g.user["_id"])
        return jsonify({"message": "Todo created successfully"}), 201

@bp.route('/<id>/update', methods=['PUT'])
@auth.login_required
def update(id):
    name = request.json.get('name')
    description = request.json.get('description')
    completed = request.json.get('completed', False)
    error = None

    if not name:
        error = 'Name is required.'
    if not description:
        error = 'Description is required.'

    if error is not None:
        return jsonify({"error": error}), 400
    else:
        success = db_handler.update_todo(id, name, description, completed, g.user["_id"])
        if success:
            return jsonify({"message": "Todo updated successfully"}), 200
        else:
            return jsonify({"error": "Todo not found"}), 404

@bp.route('/<id>', methods=['GET'])
@auth.login_required
def get_todo_by_id(id):
    todo = db_handler.get_todo_by_id(id)
    if todo:
        return jsonify(todo), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

@bp.route('/<id>/delete', methods=['DELETE'])
@auth.login_required
def delete(id):
    success = db_handler.delete_todo(id, g.user["_id"])
    if success:
        return jsonify({"message": "Todo deleted successfully"}), 200
    else:
        return jsonify({"error": "Todo not found"}), 404