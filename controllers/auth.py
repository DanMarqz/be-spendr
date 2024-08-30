import functools
import utils.db as db

from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    url_for,
    session,
    redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
db = db.DatabaseManager("users")

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'

        if error is None:
            if db.user_exists_in_database(username):
                flash('Username already exists. Choose a different one.', 'danger')
            else:
                db.register_user_in_database(username, generate_password_hash(password))
                flash('Registration successful. You can now log in.', 'success')

                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtenemos el nombre de usuario y la contraseña del formulario
        username = request.form['username']
        password = request.form['password']
        error = None

        # Validamos que se hayan ingresado el nombre de usuario y la contraseña
        if not username:
            error = 'Username es requerido'
        elif not password:
            error = 'Password es requerido'

        # Si no hay errores, buscamos al usuario en la base de datos
        if error is None:
            user = db.user_exists_in_database(username)  # Buscar usuario por nombre
            # Verificamos si el usuario existe y si la contraseña es correcta
            if user is None:
                error = 'Usuario no encontrado. Verifica el nombre de usuario.'
            elif not check_password_hash(user["password"], password):  # Verificación de contraseña
                error = 'Contraseña incorrecta. Inténtalo de nuevo.'

        # Si no hubo errores, iniciamos sesión
        if error is None:
            session.clear()  # Limpiamos cualquier sesión existente
            session['user_id'] = str(user['_id'])  # Guardamos el ID del usuario en la sesión
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('todo.index'))  # Redirigimos al índice de tareas

        # Si hubo algún error, lo mostramos al usuario
        flash(error, 'danger')

    return render_template('auth/login.html')  # Renderizamos la plantilla de login