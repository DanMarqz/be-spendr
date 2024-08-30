import utils.variables as variables

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DatabaseManager:
    def __init__(self, collection_name):
        self.__client           = MongoClient(variables.DB_URI, server_api=ServerApi('1'))
        self.__db               = self.__client[variables.DB_NAME]
        self.__db_collection    = self.__db[collection_name]

    def test_connection(self):
        print("Validating connection to database...")
        try:
            self.__client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            print(e)
            return e

    def user_exists_in_database(self, username):
        print(f"Validating if user {username} exists in database.")
        return self.__db_collection.find_one({'username': username})

    def register_user_in_database(self, username, password):
        print(f"Registering the user {username} in database. {password}")
        return self.__db_collection.insert_one({'username': username, 'password': password})

    def is_user_in_database(self, username, password):
        print(f"Validating if user {username} is registered. {password}")
        print({self.__db_collection.find_one({'username': username, 'password': password})})
        return self.__db_collection.find_one({'username': username, 'password': password})