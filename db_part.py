import mysql.connector
import sqlite3
from parser import *
from prettytable import PrettyTable

def connector_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(host = host, user = user, password = password)
        #try:
        #    print(f"Connected to MySQL server (version {conn.get_server_info()}), database {database}.")
        #except KeyError:
        #    print(f"Connected to MySQL server (version {conn.get_server_info()}), database None.")
        return conn
    except mysql.connector.Error as err:
        print(err)

def addTab(first, second):
    print(first, end='')
    for i in range(0, 22 - len(first)):
        print(" ", end='')
    if second:
        print(second)
    else:
        print("")


class workWithDb:
    def __init__(self, host, user, password, database):
        # self.dbName = title
        # self.myDb = mysql.connector.connect(
        #     host="localhost",
        #     password=password,
        #     user=user
        # )
        # self.myCursor = self.myDb.cursor()
        # self.myCursor.execute(f"CREATE DATABASE {self.dbName}")

        self.host = host
        self.user = user
        self.password = password
        self.database = database

        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")

            #self.cursor.execute("CREATE TABLE IF NOT EXISTS Requests ("
            #                   "id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, "
            #                    "h_method VARCHAR(255), url VARCHAR(255), "
            #                    "status INTEGER, params VARCHAR(255), body VARCHAR(255), "
            #                    "headers VARCHAR(255));")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Requests ("
                                "id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, "
                                "h_method VARCHAR(255), url VARCHAR(255),"
                                "body VARCHAR(255), params VARCHAR(255), headers VARCHAR(255), status INTEGER)")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Responses ("
                                "req_id INTEGER, resp_code INTEGER, result TEXT);")
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.conn = sqlite3.connect(title)
        #self.req = self.conn.cursor()
        #self.req.execute("CREATE TABLE IF NOT EXISTS Requests ("
        #                 "id INTEGER NOT NULL PRIMARY KEY autoincrement, h_method VARCHAR, url VARCHAR,"
        #                 "body VARCHAR, params VARCHAR, headers VARCHAR, status INTEGER)")
        #self.req.execute("CREATE TABLE IF NOT EXISTS Responses ("
        #                 "req_id INTEGER, resp_code INTEGER, result VARCHAR)")

    def insertIntoRequests(self, url, h_method, status, params=None, body=None, headers=None):
        sql = 'INSERT INTO Requests (h_method, url, body, params, headers, status) ' \
              f'VALUES ("{h_method}", "{url}", "{body}", "{params}", "{headers}", {status})'

        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(sql)

            lastrowid = self.cursor.lastrowid
            self.conn.commit()
            self.conn.close()

            return lastrowid
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(sql)
        #self.conn.commit()
        #return self.req.lastrowid

    def updateRequests(self, req_id, url, h_method, status, params=None, body=None, headers=None):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"UPDATE Requests SET "
                                 f'h_method = "{h_method}", url = "{url}", body = "{body}",'
                                 f'params = "{params}", headers = "{headers}, status = {status}" '
                                 f"WHERE id = {req_id};")
            self.conn.commit()
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)


        #self.req.execute(f"UPDATE Requests SET "
        #                 f'h_method = "{h_method}", url = "{url}", body = "{body}",'
        #                 f'params = "{params}", headers = "{headers}, status = {status}" '
        #                 f"WHERE id = {req_id};")
        #self.conn.commit()

    def selectRequests(self, req_id):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"SELECT * FROM Requests WHERE id = {req_id}")
            self.conn.commit()
            data = self.cursor.fetchall()
            x = PrettyTable()
            if data:
                if data[0]:
                    data = data[0]
                x.add_column('..', ['Method', 'URL', 'Params', 'Headers', 'Request body', 'Status'])
                x.add_column('Request info', [data[1], data[2], data[4], data[5], data[3], data[6]])
            print(x)
            print("---Response---")
            self.cursor.execute(f"SELECT * FROM Responses WHERE req_id = {req_id}")
            self.conn.commit()
            data = self.cursor.fetchall()
            if data:
                if data[0][2]:
                    print(data[0][2])
                else:
                    print(f"Response code = {data[0][1]}")

            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"SELECT * FROM Requests WHERE id = {req_id}")
        #self.conn.commit()
        #data = self.req.fetchall()
        #x = PrettyTable()
        #if data:
        #    if data[0]:
        #        data = data[0]
        #    x.add_column('..', ['Method', 'URL', 'Params', 'Headers', 'Request body', 'Status'])
        #    x.add_column('Request info', [data[1], data[2], data[4], data[5], data[3], data[6]])
        #print(x)
        #print("---Response---")
        #self.req.execute(f"SELECT * FROM Responses WHERE req_id = {req_id}")
        #self.conn.commit()
        #data = self.req.fetchall()
        #if data:
        #    if data[0][2]:
        #        print(data[0][2])
        #    else:
        #        print(f"Response code = {data[0][1]}")

    def deleteFromRequests(self, req_id):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"DELETE FROM Requests WHERE id = {req_id};")
            self.conn.commit()
            print(self.cursor.rowcount, "record deleted.")
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"DELETE FROM Requests WHERE id = {req_id};")
        #self.conn.commit()
        #print(self.req.rowcount, "record deleted.")

    def insertIntoResponses(self, req_id, resp_code, result={}):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute("INSERT INTO Responses (req_id, resp_code, result)"
                                f'VALUES({req_id}, {resp_code}, "{result}")')
            self.conn.commit()
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute("INSERT INTO Responses (req_id, resp_code, result)"
        #                 f'VALUES({req_id}, {resp_code}, "{result}")')
        #self.conn.commit()

    def updateResponses(self, req_id, resp_code, result):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"UPDATE Responses SET "
                                 f'resp_code = {resp_code}, result = "{result}" '
                                 f"WHERE id = {req_id}")
            self.conn.commit()
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"UPDATE Responses SET "
        #                 f'resp_code = {resp_code}, result = "{result}" '
        #                 f"WHERE id = {req_id}")
        #self.conn.commit()

    def deleteFromResponses(self, req_id):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"DELETE FROM Responses WHERE id = {req_id};")
            self.conn.commit()
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"DELETE FROM Responses WHERE id = {req_id};")
        #self.conn.commit()

    def history_show(self):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")

            print('---Request history---')
            self.cursor.execute(f"SELECT * FROM Requests")
            x = PrettyTable()
            x.field_names = ['..', 'Method', 'URL', 'Request body', 'Params', 'Headers', 'Status']
            selected = self.cursor.fetchall()
            num = len(selected)
            if num > 10:
                num = 10
            for i in range(0, num):
                x.add_row(selected[i])
            print(x.get_string(fields=['..', 'Method', 'URL', 'Request body', 'Params', 'Status']))
            req_id = input('Enter request index to view full info, or "q" to quit: ')
            while req_id != 'q':
                self.selectRequests(int(req_id))
                req_id = input('Enter request index to view full info, or "q" to quit: ')

            self.conn.close()
        except mysql.connector.Error as err:
            print(err)


        #print('---Request history---')
        #self.req.execute(f"SELECT * FROM Requests")
        #x = PrettyTable()
        #x.field_names = ['..', 'Method', 'URL', 'Request body', 'Params', 'Headers', 'Status']
        #num = 10
        #selected = self.req.fetchall()
        #for i in range(0, num):
        #    x.add_row(selected[i])
        #print(x.get_string(fields=['..', 'Method', 'URL', 'Request body', 'Params', 'Status']))
        #req_id = input('Enter request index to view full info, or "q" to quit: ')
        #while req_id != 'q':
        #    self.selectRequests(int(req_id))
        #    req_id = input('Enter request index to view full info, or "q" to quit: ')

    def history_clear(self):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute("DELETE FROM Responses")
            self.cursor.execute("DELETE FROM Requests")
            self.conn.commit()
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)

        #print('---Request history cleared---')
        #self.req.execute("DELETE FROM Responses")
        #self.req.execute("DELETE FROM Requests")
        #self.conn.commit()

    def fetchallForFilling(self):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"SELECT * FROM Requests")
            fetchall = self.cursor.fetchall()
            self.conn.commit()
            self.conn.close()

            return fetchall
        except mysql.connector.Error as err:
            print(err)
