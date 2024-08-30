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
import auth.login_required as login_required

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
  db, c = get_db()
  c.execute(
    'SELECT t.id, t.description, u.username, t.completed, t.created_at FROM todo t JOIN "todo-users" u on t.created_by = u.id order by created_at desc'
  )
  todos = c.fetchall()
  
  return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  if request.method == 'POST':
    description = request.form['description']
    error = None
    
    if not description:
      error = 'Description required'
    
    if error is not None:
      flash(error)
    else:
      db, c = get_db()
      c.execute(
        'INSERT INTO "todo" (description, completed, created_by)'
        ' values (%s, %s, %s)',
        (description, False, g.user['id'])
      )
      db.commit()
      return redirect(url_for('todo.index')) 
      
  return render_template('todo/create.html')

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    return ''