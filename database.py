import mysql.connector
class Database:

    database = None
    cursor = None

    @staticmethod
    def connect():
        Database.database = mysql.connector.connect(
            host="jackatkins.dev",
            user="jack",
            password="F9we7t4f",
            #password="xLmNN^&099nm>",
            database="site_database",
            autocommit=True,
        )
        Database.cursor = Database.database.cursor()

    @staticmethod
    def disconnect():
        if Database.database:
            Database.database.close()
            Database.cursor.close()