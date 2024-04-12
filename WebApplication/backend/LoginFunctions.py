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

'''
For route /login
    Request format
    {
     "username": username,
     "password": passord,
} 
'''     
def sign_in(request, dbClient):  # Returns Json
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbClient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:
       # print(user)
       # print(user.get("OTP"))
        account_password = cypher.decrypt(user['password'])
        if user.get("OTP") is None:
            if password == account_password:
                return {'message': 'Authorized',
                        'access': True, }
            else:
                return {'message': 'Not Authorized, incorrect password',
                        'access': False, }
        else:
            return {'message': 'Not Verified User',
                        'access': False, }
    else:
        return {'message': 'User does not exist',
                'access':False, }


'''
For route /create_user
    Request format
    {
     "username": username,
     "password": passord,
} 
''' 

def sign_up(request, dbclient):  # Returns Json
    print('start')
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})

    if user is None:
        OTP = 0000
        while user is None: 
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': temp}) is None:      # Creates Unique OTPs 
                OTP = temp
                break
        newUser = {
            "username": username,
            "password": cypher.encrypt(password),
            "systems": [],
            "notifications": [],
            "OTP": OTP,
            "sys_invites": [],
        }
        user_collection.insert_one(newUser)
        subject = "MyAPWS Account Creation: Verify Email"            # Sends Email for New User to Verify Email
        MessageFunctions.send_email(subject, username, case=1, code=OTP)  # Parameter '1' = New User Email format to send
        return {'message': 'User added.',           # TODO Need Catch Block for emails that aren't valid!!
                'access': True }
    else:
        return {'message': 'Username exists already.', 
                'access': False}
    
def forgot_request(request, dbclient):          # Creates OTP for exisiting users
    data = request.get_json()
    user_collection = dbclient.Users.User
    username = data['username'].lower()
    user = user_collection.find_one({'username': username})

    if user_exists(username, dbclient):
        OTP = 0000
        while user:
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': OTP}) is None:      # Generates unique OTP
                OTP = temp
                break
        update = {"$set": {"OTP": OTP}}
        user_collection.update_one(user, update)                    # Adds OTP to the user's document
        subject = "MyAPWS Password Reset"                           # Sends Forgot Password Email 
        MessageFunctions.send_email(subject, username, case=2, code=OTP) # Parameter '1' = New User Email format to send
        return {'access': True, 'message': 'Email has been sent'}
    else:
        return {'message': 'Username does not exist',
                'access': False, }
    
def otp_verify(request, dbclient):      # Checks to see input code matches the OTP
    data = request.get_json()
    user_collection = dbclient.Users.User
    username = data['username'].lower()
    input_otp = data['OTP']
    user = user_collection.find_one({'username': username})
    if int(user['OTP']) == int(input_otp):                            # Compares OTP from User input and Database
        remove = {"$unset": {"OTP": ""}}                    # Removes OTP from DB so it can't be used again
        user_collection.update_one(user, remove)
        return {'access': True, }
    else:
        return {'message': 'Incorrect Code', 
                'access': False, }
    
def reset_password(request, dbclient):      # Changes User Password
    data = request.get_json()
    user_collection = dbclient.Users.User
    user = user_collection.find_one({'username': username})

    username = data['username'].lower()
    new_password = data['new_password']

    update = {"$set": {"password": cypher.encrypt(new_password)}}
    user_collection.update_one(user, update)
