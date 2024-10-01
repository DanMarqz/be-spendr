import functools
from flask import Blueprint, flash, g, jsonify, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash  
import config.variables as variables
import services.db_handler as db_handler   

bp = Blueprint('auth', __name__, url_prefix='/auth')
db_handler = db_handler.DBHandler("users")

@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None  
        is_user_registered = db_handler.user_exists(username)

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if is_user_registered:
                return jsonify({"error": "Username already exists. Choose a different one."}), 400
            else:
                db_handler.add_user(username, generate_password_hash(password))
                return jsonify({"message": "Registration successful. You can now log in."}), 201

        return jsonify({"error": error}), 400

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user = db_handler.get_user_credentials(username)
            try:
                if user is None:
                    error = 'User not found. Please check the username.'
                elif not check_password_hash(user["password"], password):
                    error = 'Invalid password, please try again.'
            except Exception as e:
                print(f"{variables.ERROR_MSG} Obtaining user credentials for authentication, details: {e}")
                return jsonify({"error": 'User not registered, please register.'}), 400

        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])
            return jsonify({"message": "Login successful."}), 200

        return jsonify({"error": error}), 400

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_handler.get_user_by_id(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({"error": "Authentication required."}), 401

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Finished session."}), 200