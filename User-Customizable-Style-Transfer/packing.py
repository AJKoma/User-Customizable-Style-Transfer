import pymysql
import hashlib

class MysqlHelper():
    def __init__(self, host, database, user, password, port=3306,charset='utf8'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def select_one(self, sql, params=[]):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def select_all(self, sql, params=[]):
        result = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return result

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count

    def insert(self, sql, params=[]):
        return self.__edit(sql, params)

    def update(self, sql, params=[]):
        return self.__edit(sql, params)

    def delete(self, sql, params=[]):
        return self.__edit(sql, params)

    def my_md5(self,pwd):
        my_md5=hashlib.md5()
        my_md5.update(pwd.encode('utf-8'))
        return my_md5.hexdigest()



