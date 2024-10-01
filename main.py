from flask import Flask, jsonify

import services.db_handler as db_handler
import config.variables as variables

import controllers.auth as auth
import controllers.todo as todo

# Cargar variables de entorno
variables.loaded()

# Inicializar el manejador de base de datos
db_handler = db_handler.DBHandler(variables.DB_NAME)

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuraciones de la app
    app.config.from_mapping(
        SECRET_KEY=variables.APP_SECRET_KEY,
    )

    # Registrar Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    # Definir algunas rutas simples
    @app.route('/status')
    def status():
        return jsonify({"message": "Spendr is alive!"}), 200 

    @app.route("/test-db-connection")
    def test_db_connection():
        connection_status = db_handler.validate_connection()
        return jsonify({"connection_status": connection_status}), 200

    app.run(
        debug=variables.DEBUG_MODE,  # Se recomienda desactivar en producción
        host="0.0.0.0", 
        port=variables.PORT
    )

# Esta parte solo es necesaria cuando se ejecuta directamente con `python main.py`,
# pero no afecta cuando se usa con Gunicorn, ya que Gunicorn busca la función `create_app`.
if __name__ == "__main__":
    print(f"~~~~>_  VERSION: {variables.VERSION}")
    create_app()
