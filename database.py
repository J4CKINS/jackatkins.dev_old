import mysql.connector
class Database:

    database = None
    cursor = None

    @staticmethod
    def connect():
        Database.database = mysql.connector.connect(
            host="jackatkins.dev",
            user="app",
            password="xLmNN^&099nm>",
            auth_plugin="mysql_native_password",
            database="jackatkins_dev",
            autocommit=True,
        )
        Database.cursor = Database.database.cursor()

    @staticmethod
    def disconnect():
        if Database.database:
            Database.database.close()
            Database.cursor.close()

    @staticmethod
    def formatDatestamp(datestamp):
        day     = datestamp.strftime("%d")
        month   = datestamp.strftime("%m")
        year    = datestamp.strftime("%Y")
        return day, month, year

    @staticmethod
    def getUserAccount(username):
        Database.connect()
        Database.cursor.execute('SELECT * FROM tblUsers WHERE user=%s;', (username,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        return data
    
    @staticmethod
    def updateUserToken(userID, token):
        Database.connect()
        Database.cursor.execute('UPDATE tblUsers SET token=%s WHERE id=%s;', (token, userID))
        Database.disconnect()

    @staticmethod
    def getUserToken(userID):
        Database.connect()
        Database.cursor.execute('SELECT token FROM tblUsers WHERE id=%s;', (userID,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        return data[0]
