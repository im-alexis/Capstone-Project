#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password

import cypher

#system_collection = dbclient.Systems.System
 
def user_exists(username, dbClient):
    user_collection = dbClient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:  
        return True
    else:
        return False
      
def sign_in(request, dbClient):  # Returns Json
    username = request.form['username']
    password = request.form['password']
    user_collection = dbClient.Users.User
    user = user_collection.find_one({'username': username})
    if user is not None:
        account_password = cypher.decrypt(user['password'])
        if password == account_password:
            return {'message': 'Authorized',
                    'access': True, }
        else:
            return {'message': 'Not Authorized, incorrect Password',
                    'access': False, }
    else:
        return {'message': 'User does not exist',
                'access':False, }


def sign_up(request, dbclient):  # Returns Json
    username = request.form['username']
    password = request.form['password']
    print(request.form['username'])
    print(request.form['password'])
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
    
def password_reset(request, dbclient):
    username = request.form['username']
    if user_exists(username):
        #Send an email -> Look into mailtrap
        return {'message': 'Sent email', }
    else:
        return {'message': 'Username does not exist', }