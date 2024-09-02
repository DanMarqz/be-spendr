from flask import Flask

import utils.db as db
import utils.variables as variables

import controllers.auth as auth
import controllers.todo as todo

variables.loaded()
db = db.DatabaseManager("test")

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=variables.APP_SECRET_KEY,
    )

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    @app.route('/home')
    def home():
        return '<h1> Welcome to Spendr </h1>'

    @app.route("/test-db-connection")
    def test_db_connection():
        print(db.test_connection)
        return f"<p> {db.test_connection()} </p>"

    return app

if __name__ == "__main__":
    print(f"~~~~>_  VERSION: {variables.VERSION}")
    app = create_app() # Create the Flask app instance
    app.run(
        debug=True, 
        host="0.0.0.0", 
        port=variables.PORT
    )