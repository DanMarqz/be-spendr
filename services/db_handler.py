import datetime
import config.variables as variables  # Importamos variables de configuración (como la URI y el nombre de la base de datos)

from pymongo.mongo_client import MongoClient  # Para crear un cliente de MongoDB y conectarnos a la base de datos
from pymongo.server_api import ServerApi  # Para especificar la versión de la API del servidor MongoDB
from pymongo.errors import ConnectionFailure, OperationFailure

from bson.objectid import ObjectId

# Definimos una clase que manejará las operaciones con la base de datos
class DBHandler:
    def __init__(self, collection_name):
        self.__client           = MongoClient(variables.DB_URI, server_api=ServerApi('1'))
        self.__db               = self.__client[variables.DB_NAME]
        self.__db_collection    = self.__db[collection_name]

    ########## CONNECTION METHODS ##########

    # Método para probar la conexión a la base de datos
    def validate_connection(self) -> str:
        print("Validating connection to database...")

        try:
            self.__client.admin.command('ping')
            return "You successfully connected to Database!"
        except ConnectionFailure as e:
            return f"{variables.ERROR_MSG} Validate the connection to database, details: {e}"

    # Método para cerrar la conexión a la base de datos
    def disconnect(self) -> None:
        return self.__client.close()

    ########## END OF CONNECTION METHODS ##########

    ########## GENERAL METHODS ##########

    def get_doc_by_id(self, id):
        doc_by_id = self.__db_collection.find_one({'_id': ObjectId(id)})
        if doc_by_id:
            return doc_by_id
        else:
            return False

    ########## END OF GENERAL METHODS ##########

    ########## USER METHODS ##########

    # Método para verificar si un usuario está registrado en la base de datos
    def user_exists(self, username) -> bool:
        print(f"Validating if user {username} exists in database.")

        try:
            is_user_registered = bool(self.__db_collection.find_one({'username': username}))
            return is_user_registered
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Validate if user exists in database, details: {e}")
            return False

    # Método para registrar un nuevo usuario en la base de datos
    def add_user(self, username, password) -> bool:
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
            user_by_id = self.get_doc_by_id(id)
            return user_by_id
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user credentials for authentication, details: {e}")
            return False

    ########## END OF USER METHODS ##########

    ########## TODO METHODS ##########

    # Método para crear un todo a un usuario 
    def add_todo(self, name, description, completed, created_by):
        print(f"Registering a new todo in database.")

        try:
            self.__db_collection.insert_one(
                {
                    'name': name, 
                    'description': description, 
                    'completed': completed, 
                    'created_by': created_by,
                    'created_at': datetime.datetime.now(tz=datetime.timezone.utc),
                }
            )
            print("Todo registered in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Register a new todo in database, details: {e}")
            return False

    # Método para obtener los todos de un usuario por su id
    def get_todo_by_user_id(self, id):
        user_id = ObjectId(id)
        print(f"Obtaining user ${user_id} todos by id.")

        try:
            todos_by_id = self.__db_collection.find({'created_by': user_id})

            if todos_by_id:
                return list(todos_by_id)
            else:
                return False
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user todos, details: {e}")
            return False

    # Método para obtener un todo por su id
    def get_todo_by_id(self, id):
        print(f"Obtaining todo by id.")
        try:
            todo_by_id = self.get_doc_by_id(id)
            print(todo_by_id)
            return todo_by_id
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining todo by id, details: {e}")
            return False
 
    def update_todo(self, id, name, description, completed, created_by):
        print(f"Updating todo by id.")
        try:
            self.__db_collection.update_one(
                {
                    '_id': ObjectId(id),
                    'created_by': ObjectId(created_by)
                },
                {
                    '$set': {
                        'name': name, 
                        'description': description, 
                        'completed': completed
                    }
                }
            )
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Updating todo by id, details: {e}")
            return False

    def delete_todo(self, id, created_by):
        print(f"Deleting todo by id.")
        try:
            self.__db_collection.delete_one(
                {
                    '_id': ObjectId(id), 
                    'created_by': ObjectId(created_by)
                }
            )
            print("Todo deleted in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Deleting todo by id, details: {e}")
            return False

    ########## END OF TODO METHODS ##########re as e:
            print(f"{variables.ERROR_MSG} Deleting todo by id, details: {e}")
            return False

    ########## END OF TODO METHODS ##########
            is_user_registered = bool(self.__db_collection.find_one({'username': username}))
            return is_user_registered
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Validate if user exists in database, details: {e}")
            return False

    # Método para registrar un nuevo usuario en la base de datos
    def add_user(self, username, password) -> bool:
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
            user_by_id = self.get_doc_by_id(id)
            return user_by_id
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user credentials for authentication, details: {e}")
            return False

    ########## END OF USER METHODS ##########

    ########## TODO METHODS ##########

    # Método para crear un todo a un usuario 
    def add_todo(self, name, description, completed, created_by):
        print(f"Registering a new todo in database.")

        try:
            self.__db_collection.insert_one(
                {
                    'name': name, 
                    'description': description, 
                    'completed': completed, 
                    'created_by': created_by,
                    'created_at': datetime.datetime.now(tz=datetime.timezone.utc),
                }
            )
            print("Todo registered in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Register a new todo in database, details: {e}")
            return False

    # Método para obtener los todos de un usuario por su id
    def get_todo_by_user_id(self, id):
        user_id = ObjectId(id)
        print(f"Obtaining user ${user_id} todos by id.")

        try:
            todos_by_id = self.__db_collection.find({'created_by': user_id})

            if todos_by_id:
                return list(todos_by_id)
            else:
                return False
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining user todos, details: {e}")
            return False

    # Método para obtener un todo por su id
    def get_todo_by_id(self, id):
        print(f"Obtaining todo by id.")
        try:
            todo_by_id = self.get_doc_by_id(id)
            print(todo_by_id)
            return todo_by_id
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Obtaining todo by id, details: {e}")
            return False
 
    def update_todo(self, id, name, description, completed, created_by):
        print(f"Updating todo by id.")
        try:
            self.__db_collection.update_one(
                {
                    '_id': ObjectId(id),
                    'created_by': ObjectId(created_by)
                },
                {
                    '$set': {
                        'name': name, 
                        'description': description, 
                        'completed': completed
                    }
                }
            )
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Updating todo by id, details: {e}")
            return False

    def delete_todo(self, id, created_by):
        print(f"Deleting todo by id.")
        try:
            self.__db_collection.delete_one(
                {
                    '_id': ObjectId(id), 
                    'created_by': ObjectId(created_by)
                }
            )
            print("Todo deleted in Database")
            return True
        except OperationFailure as e:
            print(f"{variables.ERROR_MSG} Deleting todo by id, details: {e}")
            return False

    ########## END OF TODO METHODS ##########