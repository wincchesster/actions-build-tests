import pymysql

class Mysql:
    def __init__(self, host="localhost", user="user", password='password', database="database"):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
    