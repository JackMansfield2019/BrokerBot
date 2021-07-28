import psycopg2


class DatabaseUtil(object):
    def __init__(self, config):
        self.con = psycopg2.connect(host=config["host"],
                                    user=config["user"],
                                    password=config["password"],
                                    database=config["db"],
                                    port=config["port"])
        cur = self.con.cursor()
        cur.execute("SET search_path TO " + config['schema'])

    def get_con(self):
        return self.con

    def get_cur(self):
        cur = self.con.cursor()
        return cur

    def commit(self):
        self.con.commit()

    # creates table
    def create_table(self, table_name, fields):
        fields = ", ".join(["{} {}".format(i[0], i[1]) for i in fields])
        qry = """CREATE TABLE {} ({})""".format(table_name, fields)
        cur = self.get_cur()
        cur.execute(qry)
        self.commit()
        print("Table {} created".format(table_name))
