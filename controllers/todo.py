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
db = db.DatabaseManager("todo")

@bp.route('/')
@auth.login_required
def index():
    todos = db.get_todo_by_user_id(g.user["_id"])

    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@auth.login_required
def create():
  if request.method == 'POST':
    description = request.form['description']
    error = None

    if not description:
      error = 'Description required'

    if error is not None:
      flash(error)
    else:
        db.create_todo(description, False, g.user["_id"])
        return redirect(url_for('todo.index'))

  return render_template('todo/create.html')

@bp.route('/update', methods=['GET', 'POST'])
@auth.login_required
def update():
    return ''