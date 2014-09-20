import sqlite3

class DatabaseHandler:
    def __init__(self,databaseName):
        self.connection=sqlite3.connect(databaseName+".db")
        self.dataCursor = self.connection.cursor()
        self.table="mainlist"

    def readData(self):
        return self.dataCursor.execute("SELECT Name,Visits,Discount,Phone,Company FROM {0}".format(self.table)).fetchall()

    def addData(self,values):
        self.dataCursor.execute("INSERT INTO {0} VALUES({1})".format(self.table,' ,'.join(values)))
        self.connection.commit()
                                
    def updateData(self,name,phone,values):
        self.dataCursor.execute("UPDATE {0} SET Name={1},Phone={4},Visits={2},Discount={3},Company={5} WHERE Name='{6}' AND Phone='{7}'"
                                .format(self.table,values[0],values[1],values[2],values[3],values[4],name,phone))
        self.connection.commit()


    def deleteData(self,name,phone):
        self.dataCursor.execute("DELETE FROM {0} WHERE Name='{1}' AND Phone='{2}'".format(self.table,name,phone))
        self.connection.commit()

    def organizeData(self):
        self.dataCursor.execute("VACUUM {0}".format(self.table))
        self.connection.commit()

        
