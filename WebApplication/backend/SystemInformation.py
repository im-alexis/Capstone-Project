#AWPS: Backend
# Home of System Infomation Display:
#   1) /dashboard (Return the most reacent data_packet of each systemt the user is part of)
#   2) /history (Return a specific system's data array )
#   3) /system - Might be obselete but if used can return  (system users/ history / join requests )
#   4) /system_users - (Returns the array of users(w/ thier role) of a given system)
#   5) /notifications
from bson import ObjectId
from datetime import datetime


'''
# /history
    #Request format
     {
     "username": username,
      "systemID": someID,
    }
'''
def get_history (request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    user = user_collection.find_one({"username": username}, {"systems": 1})
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
                    },
                    "success": True,
                }
            else:
                return {'message': "User does not have access","success": False,}
        else:
            return {'message': "System does not exist","success": False,}
    else:
        return {'message': "User does not exist","success": False,}
    
'''
/system_users
    Request format
    {
     "username": username,
     "systemID": someID,
}
'''
def get_sys_users (request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    user = user_collection.find_one({"username": username}, {"systems": 1})
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
                        'users': system.get("users"),
                    },
                }
            else:
                return {'message': "User does not have access",}
        else:
            return {'message': "System does not exist",}
    else:
        return {'message': "User does not exist",}


'''
/system - Will return everything (user list, data, notis, requests)
    Request format
    {
     "username": username,
     "systemID": someID,
    }

'''

def sys_info(request, dbClient):
    data = request.get_json()
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

    
 
def system_collect(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    user_system_id= []
    
    user = user_collection.find_one({"username": username})
    

    if user is not None:
        user_sys_arr = user.get("systems", [])
        for entry in user_sys_arr:
            user_system_id.append(entry['systemID']) # { "message": [ "test123", "a2h87hd1" ] }


    system_data_packets = {}
    for system_id in user_system_id:
        system = system_collection.find_one({"systemID": system_id})

        if system:
            data_packets = system.get("data_packets", [])
            if data_packets:
                system_data_packets[system_id] = data_packets[-1]

    return {
        'message': system_data_packets,
         }

def dashboard_data(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    user = user_collection.find_one({"username": username}, {"systems": 1})
    if user is None:
        return {'message': username + " does not exist"}

    systems_arr = user.get('systems', [])
    system_ids = [system['systemID'] for system in systems_arr]
    
    # Retrieve the latest data packet for each system in a single query
    cursor = system_collection.aggregate([
        {"$match": {"systemID": {"$in": system_ids}}},
        {"$project": {
            "systemID": 1,
            "latestDataPacket": {"$arrayElemAt": ["$data_packets", -1]}
        }}
    ])

    ret_arr = []
    for system_data in cursor:
        ret_arr.append({
            'systemID': system_data['systemID'],
            'data_packet': system_data['latestDataPacket']
        })

    return {'message': ret_arr}