from .DButil import DatabaseUtil
import json
from passlib.hash import pbkdf2_sha256

with open("config.json", "r") as file:
    config = json.load(file)


class Users(object):
    def __init__(self):
        self.db = DatabaseUtil(config["Database"])
        self.user_fields = [("id", "SERIAL PRIMARY KEY"), ("username_", "VARCHAR(225)"),
                            ("password_", "VARCHAR(225)")]

    def set_up_db(self):
        self.db.create_table("BrokerBot_configuration_Users", self.user_fields)

    # returns a tuple of two ints
    # tuple[0] = 0 if user is not found, = 1 if user is found
    # tuple[1] = 0 if user is not added to database, = 1 is user is added
    def insert_data_for_Users(self, username, password):
        found = self.find_user(username, password)
        if found != 0:
            print("Username already exists.")
            return 1, 0
        else:
            try:
                qry = """insert into
                        BrokerBot_configuration_Users(username_, password_)
                        values('%s', '%s')""" % (username, pbkdf2_sha256.encrypt(password))
                cur = self.db.get_cur()
                cur.execute(qry)
                self.db.commit()
                print("%s added" % username)
                return 0, 1
            except:
                return 0, 0

    def get_user(self, username):
        qry = """select * from brokerbot_configuration_users where 
                username = '%s'""" % username
        cur = self.db.get_cur()
        cur.execute(qry)
        users = cur.fetchall()
        return users

    def find_user(self, username, password):
        users = self.get_user(username)
        if len(users) == 0:
            return 0
        for user in users:  # check for all users returned if their password is the same as the given password
            if pbkdf2_sha256.verify(password, user[2]):
                return 1
        return 2


class Bots(object):
    def __init__(self):
        self.db = DatabaseUtil(config["Database"])
        self.bot_fields = [("bot_id", "bigint PRIMARY KEY"), ("user_id", "bigint"),
                           ("alpaca_key", "VARCHAR(225)")]

    def set_up_db(self):
        self.db.create_table("BrokerBot_configuration_Bots", self.bot_fields)

    def insert_data_for_Bots(self, bot_id, user_id, key):
        qry = """insert int BrokerBot_configuration_Bots(bot_id, user_id, alpaca_key)
        values('%s', '%s', '%s')""" % (bot_id, user_id, key)
        cur = self.db.get_cur()
        cur.execute(qry)
        self.db.commit()
        print("Bot %s added\n" % bot_id)

    def find_bots(self, user_ID):
        bots = self.get_bots(user_ID)
        if len(bots) == 0:
            return 0
        return 1

    def get_bots(self, user_ID):
        qry = """select * from BrokerBot_configuration_Bots where user_id = '%s'""" % user_ID
        cur = self.db.get_cur()
        cur.execute(qry)
        bot = cur.fetchall()
        return bot
