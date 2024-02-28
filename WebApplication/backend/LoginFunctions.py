#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password

from pymongo import MongoClient
import cypher

# to access the database w/o certifi add this: &tlsAllowInvalidCertificates=true at the end of url
client = MongoClient(
    "mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")
systems_db = client.Systems
users_db = client.Users
user_collection = users_db.User
system_collection = users_db.Systems

def user_exists(username):
    user = user_collection.find_one({'username': username})
    if user is not None:  
        return True
    else:
        return False
      
def sign_in(username, password):  # Returns Json
    user = user_collection.find_one({'username': username})
    if user is not None:
        account_password = cypher.decrypt(user['password'])
        if password == account_password:
            return {'message': 'Authorized', }
        else:
            return {'message': 'Not Authorized, incorrect Password', }
    else:
        return {'message': 'User does not exist', }


def sign_up( username, password):
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
    
def password_reset(username):
    if user_exists(username):
        #Send an email
        return {'message': 'Sent email', }
    else:
        return {'message': 'Username does not exist', }