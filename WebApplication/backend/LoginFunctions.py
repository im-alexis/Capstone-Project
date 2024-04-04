#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password

import cypher
import random
import MessageFunctions

#system_collection = dbclient.Systems.System
 
def user_exists(username, dbClient):
    user_collection = dbClient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:  
        return True
    else:
        return False

# For route /
    #Request format
#     {
#      "username": username,
#      "password": passord,
# }      
def sign_in(request, dbClient):  # Returns Json
    # username = request.form['username']
    # password = request.form['password']
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbClient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:
        account_password = cypher.decrypt(user['password'])
        if password == account_password:
            return {'message': 'Authorized',
                    'access': True, }
        else:
            return {'message': 'Not Authorized, incorrect password',
                    'access': False, }
    else:
        return {'message': 'User does not exist',
                'access':False, }


def sign_up(request, dbclient):  # Returns Json
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})

    if user is None:
        OTP = 0000
        while user:
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': OTP}) is None:
                OTP = temp
                break
        newUser = {
            "username": username,
            "password": cypher.encrypt(password),
            "systems": [],
            "notifications": [],
            "OTP": OTP,
        }
        user_collection.insert_one(newUser)
        subject = "MyAPWS Account Creation: Verify Email"
        MessageFunctions.send_email(subject, username, 1)
        return {'message': 'User added.', }
    else:
        return {'message': 'Username exists already.', }
    
def forgot_request(request, dbclient):
    data = request.get_json()
    user_collection = dbclient.Users.User
    username = data['username'].lower()
    user = user_collection.find_one({'username': username})

    if user_exists(username):
        OTP = 0000
        while user:
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': OTP}) is None:
                OTP = temp
                break
        update = {"$set": {"OTP": OTP}}
        user_collection.update_one(user, update)
        subject = "MyAPWS Password Reset"
        MessageFunctions.send_email(subject, username, 2)
        return {'access': True, }
    else:
        return {'message': 'Username does not exist',
                'access': False, }
    
def otp_verify(request, dbclient):
    data = request.get_json()
    user_collection = dbclient.Users.User
    username = data['username'].lower()
    input_otp = data['OTP']
    user = user_collection.find_one({'username': username})
    if user['OTP'] == input_otp:
        remove = {"$unset": {"OTP": ""}}
        user_collection.update_one(user, remove)
        return {'access': True, }
    else:
        return {'message': 'Incorrect Code', 
                'access': False, }
    
def reset_password(request, dbclient):
    data = request.get_json()
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})

    username = data['username'].lower()
    new_password = data['new_password']

    update = {"$set": {"password": cypher.encrypt(new_password)}}
    user_collection.update_one(user, update)
