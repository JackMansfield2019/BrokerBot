import json
from .DBmanager import Users


user_db = Users()


def set_up_users():
    user_db.set_up_db()


def insert_user(username, password):
    return user_db.insert_data_for_Users(username, password)


def find_user(username, password):
    return user_db.find_user(username, password)
    
