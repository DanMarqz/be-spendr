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

import utils.db as db
import controllers.auth as auth

bp = Blueprint('todo', __name__)
db = db.DBHandler("todo")
todos = ''

@bp.route('/')
@auth.login_required
def index():
  todos = db.get_todo_by_user_id(g.user["_id"])
  return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@auth.login_required
def create():
  if request.method == 'POST':
    name = request.form['name']
    description = request.form['description']
    error = None

    if not description:
      error = 'Description required'

    if error is not None:
      flash(error)
    else:
        db.add_todo(name, description, False, g.user["_id"])
        return redirect(url_for('todo.index'))

  return render_template('todo/create.html')

@bp.route('/<id>/update', methods=['GET', 'POST'])
@auth.login_required
def update(id):

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db.update_todo(id, name, description, completed)

        return redirect(url_for('todo.index'))

    if request.method == 'GET':
        todo = db.get_todo_by_id(id)
        if todo:
            return render_template(
                'todo/update.html',
                todo={
                    "name": todo["name"],
                    "description": todo["description"],
                    "completed": todo["completed"],
                    "created_at": todo["created_at"]
                }
            )
        else:
            abort(404, description="Todo not found")

@bp.route('/<id>/delete', methods=['GET', 'POST'])
@auth.login_required
def delete():
    return ''