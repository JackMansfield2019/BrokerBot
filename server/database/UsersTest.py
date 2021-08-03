import json
from DBmanager import *


user_db = Users()
bot_db = Bots()


def set_up_users():
    user_db.set_up_db()


def insert_user(username, password):
    user_db.insert_data_for_Users(username, password)


def find_user(username, password):
    user = user_db.find_user(username, password)
    print(user)


def set_up_bots():
    bot_db.set_up_db()


set_up_bots()
