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
        if len(repeat) != 0:
            print("Username or password already exists.")
            return 1, 0
        else:
            try:
                qry = """insert into
                        BrokerBot_configuration_Users(username_, password_)
                        values('%s', '%s')""" % (username, password)
                cur = self.db.get_cur()
                cur.execute(qry)
                self.db.commit()
                print("%s added" % username)
                return 0, 1
            except:
                return 0, 0

    def find_user(self, username, password):
        qry = """select * from BrokerBot_configuration_Users where 
        username_ = '%s' and password_ = '%s'""" % (username, password)
        cur = self.db.get_cur()
        cur.execute(qry)
        users = cur.fetchall()
        return users


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
        qry = """select * from BrokerBot_configuration_Bots where user_id = '%s'""" % user_ID
        cur = self.db.get_cur()
        cur.execute(qry)
        bot = cur.fetchall()
        return bot

