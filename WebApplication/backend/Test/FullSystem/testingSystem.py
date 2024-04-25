from flask import Flask, request, session
from pymongo import MongoClient
from flask_cors import CORS

#LOOK INTO SESSIONS
app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")

def sys_info(data, dbClient):
    username = data['username'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    user = user_collection.find_one({"username": username})

    
    system = system_collection.find_one({'systemID': systemID}, {"users": 1, "data_packets": 1, "join_request": 1})
    
    if user:
        user_sys_arr = user.get("systems", [])
        if system:
            sys_usr_arr = system.get("users", [])
            
            is_member = any(entry['systemID'] == systemID for entry in user_sys_arr)
            is_member2 = any(entry['username'] == username for entry in sys_usr_arr)
            
            if is_member and is_member2:
                return {
                    'message': {
                        'systemID': systemID,
                        'data_packets': system.get("data_packets"),
                        'users': system.get("users"),
                        'join_request': system.get("join_request"),
                         'settings':system.get("settings"),
                    },
                    "success": True,
                }
            else:
                return {'message': "User does not have access","success": False,}
        else:
            return {'message': "System does not exist","success": False,}
    else:
        return {'message': "User does not exist","success": False,}

def user_systems(data, dbClient):
    username = data['username'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    user = user_collection.find_one({"username": username})

    requests = []
    if user:
        for i in range(len(user['systems'])):
            if user['systems'][i]["access_level"] > 0:
              requests.append(user['systems'][i])
    print(requests)

def wth(): # Pulling Specific System Request
  data = {"username": "kietle24@utexas.edu",
          "systemID": "a2h87hd1", }
  response = sys_info(data, client)
  print(response)
  print()
  print(response["message"]["join_request"])
# #system route
# @app.route("/system", methods=['POST'])
# def system():
#     response = SystemInformation.sys_info(request, client)
#     return response
def hmm(): # Pulling All User's Systems
    data = {"username": "kietle24@utexas.edu",
          "systemID": "a2h87hd1", }
    response = user_systems(data, client)
    print()
# wth()
hmm()