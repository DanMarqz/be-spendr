import utils.variables as variables  # Importamos variables de configuración (como la URI y el nombre de la base de datos)

from pymongo.mongo_client import MongoClient  # Para crear un cliente de MongoDB y conectarnos a la base de datos
from pymongo.server_api import ServerApi  # Para especificar la versión de la API del servidor MongoDB
from pymongo.errors import ConnectionFailure, OperationFailure

from bson.objectid import ObjectId

# Definimos una clase que manejará las operaciones con la base de datos
class DatabaseManager:
    def __init__(self, collection_name):
        self.__client           = MongoClient(variables.DB_URI, server_api=ServerApi('1'))
        self.__db               = self.__client[variables.DB_NAME]
        self.__db_collection    = self.__db[collection_name]

    # Método para probar la conexión a la base de datos
    def test_connection(self):
        print("Validating connection to database...")

        try:
            self.__client.admin.command('ping')
            return "Pinged your deployment. You successfully connected to MongoDB!"
        except ConnectionFailure as e:
            return f"{variables.ERROR_MSG} Validate the connection to database, details: {e}"

    # Método para cerrar la conexión a la base de datos
    def close_connection(self):
        return self.__client.close()

    # Método para verificar si un usuario está registrado en la base de datos
    def check_user_existence(self, username):
        print(f"Validating if user {username} exists in database.")

        try:
            is_user_registered = bool(self.__db_collection.find_one({'username': username}))
            return is_user_registered
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Validate if user exists in database, details: {e}")
            return False

    # Método para registrar un nuevo usuario en la base de datos
    def register_user_in_database(self, username, password):
        print(f"Registering the user {username} in database.")

        try:
            self.__db_collection.insert_one({'username': username, 'password': password})
            print("User registered in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Register a new user in database, details: {e}")
            return False

    # Método para obtener las credenciales de autenticacion de un usuario
    def get_user_credentials(self, username):
        print(f"Obtaining user credentials for authentication.")
        
        try:
            user_credentials = self.__db_collection.find_one({'username': username})
            if user_credentials:
                return user_credentials
            else:
                return False
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user credentials for authentication, details: {e}")
            return False

    # Método para obtener un usuario por su uid
    def get_user_by_id(self, id):
        print(f"Obtaining user credentials by id.")
        
        try:
            user_by_id = self.__db_collection.find_one({'_id': ObjectId(id)})
            if user_by_id:
                return user_by_id
            else:
                return False
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user credentials for authentication, details: {e}")
            return False

    # Método para crear un todo a un usuario 
    def create_todo(self, description, completed, created_by):
        print(f"Registering a new todo in database.")

        try:
            self.__db_collection.insert_one({'description': description, 'completed': completed, 'created_by': created_by})
            print("Todo registered in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Register a new todo in database, details: {e}")
            return False

    # Método para obtener los todos de un usuario por su id
    def get_todo_by_user_id(self, id):
        print(f"Obtaining user todos by id.")

        try:
            todos_by_id = self.__db_collection.find({'_id': ObjectId(id)})
            print(f"todos:  {todos_by_id}")
            if todos_by_id:
                return todos_by_id
            else:
                return False
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user todos, details: {e}")
            return False