#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password

from pymongo import MongoClient
import cypher

# to access the database w/o certifi add this: &tlsAllowInvalidCertificates=true at the end of url


#system_collection = dbclient.Systems.System
 
def user_exists(username, dbclient):
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:  
        return True
    else:
        return False
      
def sign_in(username, password, dbclient):  # Returns Json
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:
        account_password = cypher.decrypt(user['password'])
        if password == account_password:
            return {'message': 'Authorized',
                    'Access': True, }
        else:
            return {'message': 'Not Authorized, incorrect Password',
                    'access': False, }
    else:
        return {'message': 'User does not exist',
                'access':True, }


def sign_up( username, password, dbclient):
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})
    if user is None:
        newUser = {
            "username": username,
            "password": cypher.encrypt(password),
            "systems": [],
        }
        user_collection.insert_one(newUser)
        return {'message': 'User added.', }
    else:
        return {'message': 'Username exists already.', }
    
def password_reset(username, dbclient):
    if user_exists(username):
        #Send an email -> Look into mailtrap
        return {'message': 'Sent email', }
    else:
        return {'message': 'Username does not exist', }