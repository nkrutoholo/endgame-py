# import mysql.connector
import sqlite3
from parser import *
from prettytable import PrettyTable
import mysql.connector


def connector_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(host = host, user = user, password = password)
        try:
            print(f"Connected to MySQL server (version {conn.get_server_info()}), database {database}.")
        except KeyError:
            print(f"Connected to MySQL server (version {conn.get_server_info()}), database None.")
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

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Requests ("
                                "id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, "
                                "h_method VARCHAR(255), url VARCHAR(255), "
                                "status INTEGER, params VARCHAR(255), body VARCHAR(255), "
                                "headers VARCHAR(255));")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Responses ("
                                "req_id INTEGER, resp_code INTEGER, result VARCHAR(255));")
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)


        #self.conn = sqlite3.connect(title)
        #self.req = self.conn.cursor()
        #self.req.execute("CREATE TABLE IF NOT EXISTS Requests ("
        #                 "id INTEGER NOT NULL PRIMARY KEY autoincrement, h_method VARCHAR, url VARCHAR,"
        #                 "status INTEGER, params VARCHAR, body VARCHAR,"
        #                 "headers VARCHAR)")
        #self.req.execute("CREATE TABLE IF NOT EXISTS Responses ("
        #                 "req_id INTEGER, resp_code INTEGER, result VARCHAR)")

    def insertIntoRequests(self, url, h_method, status, params=None, body=None, headers=None):
        sql = 'INSERT INTO Requests (h_method, url, status, params, body, headers) ' \
              f'VALUES ("{h_method}", "{url}", {status}, "{params}", "{body}", "{headers}")'

        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(sql)
            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)


        #self.req.execute(sql)
        #self.conn.commit()
        #print(self.req.rowcount, "record inserted.")
        #return self.req.lastrowid

    def updateRequests(self, req_id, url, h_method, status, params=None, body=None, headers=None):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"UPDATE Requests SET "
                                 f"h_method = '{h_method}', url = '{url}', status = {status},"
                                 f'params = "{params}", body = "{body}", headers = "{headers}" '
                                 f"WHERE id = {req_id};")
            self.conn.close()

            print(self.cursor.rowcount, "record updated.")
        except mysql.connector.Error as err:
            print(err)


        #self.req.execute(f"UPDATE Requests SET "
        #                 f"h_method = '{h_method}', url = '{url}', status = {status},"
        #                 f'params = "{params}", body = "{body}", headers = "{headers}" '
        #                 f"WHERE id = {req_id};")
        #self.conn.commit()
        #print(self.req.rowcount, "record updated.")

    def selectRequests(self, req_id):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"SELECT * FROM Requests WHERE id = {req_id}")

            data = self.cursor.fetchall()
            if data:
                if data[0]:
                    data = data[0]
                print("====================  ==============")
                print("..                    Request info  ")
                print("====================  ==============")
                addTab("Method", data[1])
                addTab("URL", data[2])
                addTab("Params", dictToPrettyString(data[4], " ", 0))
                addTab("Headers", dictToPrettyString(data[6], " ", 0))
                addTab("Request body", dictToPrettyString(data[5], " ", 0))
                # self.addTab("Basic Authentication", data[7])
                addTab("Status", data[3])
                print("====================  ==============")
                print("---Response---")
            self.cursor.execute(f"SELECT * FROM Responses WHERE req_id = {req_id}")

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
        #if data:
        #    if data[0]:
        #        data = data[0]
        #    print("====================  ==============")
        #    print("..                    Request info  ")
        #    print("====================  ==============")
        #    addTab("Method", data[1])
        #    addTab("URL", data[2])
        #    addTab("Params", dictToPrettyString(data[4], " ", 0))
        #    addTab("Headers", dictToPrettyString(data[6], " ", 0))
        #    addTab("Request body", dictToPrettyString(data[5], " ", 0))
        #    # self.addTab("Basic Authentication", data[7])
        #    addTab("Status", data[3])
        #    print("====================  ==============")
        #    print("---Response---")
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
            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
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
            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute("INSERT INTO Responses (req_id, resp_code, result)"
        #                 f'VALUES({req_id}, {resp_code}, "{result}")')
        #self.conn.commit()
        #print(self.req.rowcount, "record inserted.")

    def updateResponses(self, req_id, resp_code, result):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"UPDATE Responses SET "
                                f'resp_code = {resp_code}, result = "{result}" '
                                f"WHERE id = {req_id}")
            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"UPDATE Responses SET "
        #                 f'resp_code = {resp_code}, result = "{result}" '
        #                 f"WHERE id = {req_id}")
        #self.conn.commit()
        #print(self.req.rowcount, "record updated.")

    def deleteFromResponses(self, req_id):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"DELETE FROM Responses WHERE id = {req_id};")
            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print(err)

        #self.req.execute(f"DELETE FROM Responses WHERE id = {req_id};")
        #self.conn.commit()
        #print(self.req.rowcount, "record deleted.")

    def history_show(self):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")

            print('---Request history---')
            self.cursor.execute(f"SELECT * FROM Requests")
            # print("====  ========  =============  ====================  =============  ========")
            # print("  ..  Method    URL            Params                Request body     Status")
            # print("====  ========  =============  ====================  =============  ========")
            x = PrettyTable()
            x.field_names = ['..', 'Method', 'URL', 'Status', 'Request body', 'Params', 'Headers']
            for i in self.cursor.fetchall():
                x.add_row(i)
            print(x.get_string(fields=['..', 'Method', 'URL', 'Status', 'Request body', 'Params']))
            #     for j in i:
            #         print(j, end='  ')
            #     print('\n')
            # print("====  ========  =============  ====================  =============  ========")
            req_id = input('Enter request index to view full info, or "q" to quit: ')
            while req_id != 'q':
                self.selectRequests(int(req_id))
                req_id = input('Enter request index to view full info, or "q" to quit: ')

            self.conn.close()

            print(self.cursor.rowcount, "record inserted.")
        except mysql.connector.Error as err:
            print(err)


        #print('---Request history---')
        #self.req.execute(f"SELECT * FROM Requests")
        ## print("====  ========  =============  ====================  =============  ========")
        ## print("  ..  Method    URL            Params                Request body     Status")
        ## print("====  ========  =============  ====================  =============  ========")
        #x = PrettyTable()
        #x.field_names = ['..', 'Method', 'URL', 'Status', 'Request body', 'Params', 'Headers']
        #for i in self.req.fetchall():
        #    x.add_row(i)
        #print(x.get_string(fields=['..', 'Method', 'URL', 'Status', 'Request body', 'Params']))
        ##     for j in i:
        ##         print(j, end='  ')
        ##     print('\n')
        ## print("====  ========  =============  ====================  =============  ========")
        #req_id = input('Enter request index to view full info, or "q" to quit: ')
        #while req_id != 'q':
        #    self.selectRequests(int(req_id))
        #     req_id = input('Enter request index to view full info, or "q" to quit: ')

    def history_clear(self):
        try:
            self.conn = connector_mysql(self.host, self.user, self.password, self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute("DELETE FROM Responses")
            self.cursor.execute("DELETE FROM Requests")
            self.conn.close()
        except mysql.connector.Error as err:
            print(err)


        #print('---Request history cleared---')
        #self.req.execute("DELETE FROM Responses")
        #self.req.execute("DELETE FROM Requests")
        #self.conn.commit()
