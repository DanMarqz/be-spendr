import functools
import utils.db as db   # Importamos el módulo 'utils.db' para interactuar con la base de datos

from flask import (
    Blueprint,          # Para organizar las rutas de la aplicación en un módulo
    flash,              # Para mostrar mensajes flash a los usuarios (mensajes temporales)
    g,                  # Para almacenar datos a lo largo del ciclo de la petición
    render_template,    # Para renderizar plantillas HTML
    request,            # Para acceder a los datos de la solicitud (POST, GET, etc.)
    url_for,            # Para generar URLs dinámicamente
    session,            # Para manejar la sesión del usuario
    redirect            # Para redirigir al usuario a otra página
)

# Para manejar el hashing de contraseñas
from werkzeug.security import check_password_hash, generate_password_hash  

# Definimos un blueprint llamado 'auth' con prefijo de URL '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Inicializamos el manejador de la DB para trabajar con la colección 'users'
db = db.DBHandler("users")

# Ruta para el registro de usuarios
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] # Obtenemos el nombre de usuario del formulario
        password = request.form['password'] # Obtenemos la contraseña del formulario
        error = None  # Inicializamos la variable de error
        is_user_registered = db.user_exists(username)

        # Validamos si el nombre de usuario está vacío
        if not username:
            error = 'Username es requerido'
        # Validamos si la contraseña está vacía
        if not password:
            error = 'Password es requerido'

        # Si no hay errores en los campos
        if error is None:
            # Verificamos si el usuario ya está registrado
            if is_user_registered:
                flash('Username already exists. Choose a different one.', 'danger')  # Mostramos un mensaje de error
            else:
                # Registramos el usuario en la base de datos con la contraseña encriptada
                db.add_user(username, generate_password_hash(password))
                flash('Registration successful. You can now log in.', 'success')  # Mensaje de éxito

                # Redirigimos a la página de inicio de sesión
                return redirect(url_for('auth.login'))

    # Si la solicitud es GET o hubo algún error, renderizamos el formulario de registro
    return render_template('auth/register.html')

# Ruta para el inicio de sesión
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Si la solicitud es POST, se está enviando el formulario de login
        username = request.form['username']  # Obtenemos el nombre de usuario del formulario
        password = request.form['password']  # Obtenemos la contraseña del formulario
        error = None  # Inicializamos la variable de error

        # Validamos si el nombre de usuario está vacío
        if not username:
            error = 'Username es requerido'
        elif not password:
            error = 'Password es requerido'

        # Si no hay errores en los campos
        if error is None:
            # Buscamos al usuario en la base de datos por su nombre
            user = db.get_user_credentials(username)
            # Verificamos si el usuario existe y si la contraseña es correcta
            if user is None:
                error = 'Usuario no encontrado. Verifica el nombre de usuario.'  # Usuario no encontrado
            elif not check_password_hash(user["password"], password):  # Verificación de la contraseña
                error = 'Contraseña incorrecta. Inténtalo de nuevo.'

        # Si no hubo errores, iniciamos la sesión del usuario
        if error is None:
            session.clear()  # Limpiamos cualquier sesión existente
            session['user_id'] = str(user['_id'])           # Guardamos el ID del usuario en la sesión actual
            flash('Inicio de sesión exitoso.', 'success')   # Mostramos mensaje de éxito
            return redirect(url_for('todo.index'))          # Redirigimos al índice de tareas

        # Si hubo algún error, lo mostramos al usuario
        flash(error, 'danger')

    # Si la solicitud es GET o hubo algún error, renderizamos el formulario de login
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_user_by_id(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))