from DButil import DatabaseUtil
import json

with open("config.json", "r") as file:
    config = json.load(file)


class Users(object):
    def __init__(self):
        self.db = DatabaseUtil(config["Database"])
        self.user_fields = [("id", "SERIAL PRIMARY KEY"), ("username_", "VARCHAR(225)"),
                            ("password_", "VARCHAR(225)")]

    def set_up_db(self):
        self.db.create_table("BrokerBot_configuration_Users", self.user_fields)

    def insert_data_for_Users(self, username, password):
        repeat = self.find_user(username, password)
        if repeat != 0:
            print("Username or password already exists.")
        else:
            qry = """insert into
                    BrokerBot_configuration_Users(username_, password_)
                    values('%s', '%s')""" % (username, password)
            cur = self.db.get_cur()
            cur.execute(qry)
            self.db.commit()
            print("%s added" % username)

    def find_user(self, username, password):
        qry = """select * from BrokerBot_configuration_Users where 
        username_ = '%s' and password_ = '%s'""" % (username, password)
        cur = self.db.get_cur()
        cur.execute(qry)
        users = cur.fetchall()
        if len(users) == 0:
            return 0
        else:
            return users


class Bots(object):
    def __init__(self):
        self.db = DatabaseUtil(config["Database"])
        self.bot_fields = [("bot_id", "bigint PRIMARY KEY"), ("user_id", "bigint"),
                           ("alpaca_key", "VARCHAR(225)")]

    def set_up_db(self):
        self.db.create_table("BrokerBot_configuration_Bots", self.bot_fields)
