from flask import Flask, jsonify

import services.db_handler as db_handler
import config.variables as variables

import controllers.auth as auth
import controllers.todo as todo

variables.loaded()
db_handler = db_handler.DBHandler("test")

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=variables.APP_SECRET_KEY,
    )

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    @app.route('/status')
    def status():
        return jsonify({"message": "Spendr is alive!"}), 200 

    @app.route("/test-db-connection")
    def test_db_connection():
        connection_status = db_handler.validate_connection()
        return jsonify({"connection_status": connection_status}), 200

    return app

if __name__ == "__main__":
    print(f"~~~~>_  VERSION: {variables.VERSION}")
    app = create_app()  # Create the Flask app instance
    app.run(
        debug=True, 
        host="0.0.0.0", 
        port=variables.PORT
    )