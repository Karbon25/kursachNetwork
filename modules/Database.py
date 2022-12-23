import mysql.connector
class DBClient:
    def __init__(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = ''
        self.db_name = 'projectk'
        self.connect = mysql.connector.connect(host=self.host,user=self.username,passwd=self.password,database=self.db_name)
        

    def executeSelect(self, query):
        try:
            if(self.connect != False):
                cursor = self.connect.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return(result)
            else:
                return(False)
        except:
            return(False)
    def execute(self, query):
        try:
            if(self.connect != False):
                cursor = self.connect.cursor()
                cursor.execute(query, [])
                if(cursor.rowcount != 0):
                    self.connect.commit()
                    return(cursor.lastrowid)
                cursor.close()
            else:
                return(False)
        except:
            return(False)
    def DBclose(self):
        self.connect.close()