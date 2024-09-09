import mysql.connector

class DatabaseManager:
    def __init__(self,host,port, user, password, database):
        self.host = host
        self.user = user

        self.port = port
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.operations = []  # 用于存储未提交的操作

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        """执行查询，但不立即提交"""
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

    def executemany_query(self, query, values=None):
        """执行查询，但不立即提交"""
        if values:
            self.cursor.executemany(query, values)
        else:
            self.cursor.executemany(query)

    def commit(self):
        """提交所有未提交的操作"""
        for query, values in self.operations:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
        self.connection.commit()
        self.operations = []  # 清空已提交的操作

    def fetch_all(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()