import bcrypt
import uuid
from database import Database

class Guard:
    '''A class for handling authentication for PostIt'''

    @staticmethod
    def authenticateUser(username, password):
        # Authenticates the user based on a username or password
        # If the user is successfully authenticated then the user's id and token are returned
        # If the authentication is unseccessful then the method returns false

        user = Database.getUserAccount(username)
        
        # check if any data has been retrieved
        if user:
            # check if password matches hash stored on the database
            if bcrypt.checkpw(password.encode(), user[2].encode()):
                return (
                    user[0],
                    Guard.genToken(user[0])
                )

        return False

    @staticmethod
    def authenticateUserToken(userID, token):
        userToken = Database.getUserToken(userID)
        return userToken == token

    @staticmethod
    def genToken(userID):
        token = str(uuid.uuid4())
        Database.updateUserToken(userID, token)
        return token