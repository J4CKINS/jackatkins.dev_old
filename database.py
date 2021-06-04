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

    @staticmethod
    def getBlogPosts(postedOnly=False):
        Database.connect()
        if postedOnly:
            Database.cursor.execute('SELECT * FROM tblBlogPosts WHERE posted=1 ORDER BY id DESC')
        else:
            Database.cursor.execute('SELECT * FROM tblBlogPosts ORDER BY id DESC')
        
        data = Database.cursor.fetchall()
        Database.disconnect()

        return data

    @staticmethod
    def getBlogPostByID(ID):
        Database.connect()
        Database.cursor.execute('SELECT * FROM tblBlogPosts WHERE id=%s;', (ID,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        return data

    @staticmethod
    def createBlogPost(title, content, posted):
        Database.connect()
        Database.cursor.execute('INSERT INTO tblBlogPosts (title, content, datestamp, posted) VALUES (%s, %s, now(), %s);', (title, content, posted))
        Database.disconnect()

    @staticmethod
    def updateBlogPost(ID, title, content, posted):
        Database.connect()
        Database.cursor.execute('UPDATE tblBlogPosts SET title=%s, content=%s, posted=%s WHERE id=%s;', (title, content, posted, ID))
        Database.disconnect()

    @staticmethod
    def blogPostExists(ID):
        Database.connect()
        Database.cursor.execute('SELECT id FROM tblBlogPosts WHERE id=%s;', (ID,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        if data:
            return True
        return False

    @staticmethod
    def getProjectPosts(postedOnly=False):
        Database.connect()
        if postedOnly:
            Database.cursor.execute('SELECT * FROM tblProjectPosts WHERE posted=1 ORDER BY id DESC')
        else:
            Database.cursor.execute('SELECT * FROM tblProjectPosts ORDER BY id DESC')
        
        data = Database.cursor.fetchall()
        Database.disconnect()

        return data

    @staticmethod
    def getProjectPostByID(ID):
        Database.connect()
        Database.cursor.execute('SELECT * FROM tblProjectPosts WHERE id=%s;', (ID,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        return data

    @staticmethod
    def createProjectPost(title, content, posted):
        Database.connect()
        Database.cursor.execute('INSERT INTO tblProjectPosts (title, content, datestamp, posted) VALUES (%s, %s, now(), %s);', (title, content, posted))
        Database.disconnect()

    @staticmethod
    def updateProjectPost(ID, title, content, posted):
        Database.connect()
        Database.cursor.execute('UPDATE tblProjectPosts SET title=%s, content=%s, posted=%s WHERE id=%s;', (title, content, posted, ID))
        Database.disconnect()

    @staticmethod
    def projectPostExists(ID):
        Database.connect()
        Database.cursor.execute('SELECT id FROM tblProjectPosts WHERE id=%s;', (ID,))
        data = Database.cursor.fetchone()
        Database.disconnect()
        if data:
            return True
        return False