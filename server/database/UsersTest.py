import json
from DBmanager import DBManager

with open("config.json", "r") as file:
    config = json.load(file)
database = DBManager(config)


def set_up_db():
    database.set_up_db()


def insert_user(username, password):
    database.insert_data_for_Users(username, password)


def find_user(username, password):
    user = database.find_user(username, password)
    print(user)


# set_up_db()
insert_user("username", "password")
find_user("username", "password")
