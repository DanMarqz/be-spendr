import utils.db as db

db = db.DBHandler("users")

db.validate_connection()

user_login = db.get_user_credentials("dani")
print(user_login)

user_by_id = db.get_user_by_id('66d14938ad0e93447911072a')
print(user_by_id)
db.disconnect()