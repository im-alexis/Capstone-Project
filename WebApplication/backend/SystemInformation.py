#AWPS: Backend
# Home of System Infomation Display:
#   1) /dashboard (Return the most reacent data_packet of each systemt the user is part of)
#   2) /history (Return a specific system's data array )
#   3) /system - Might be obselete but if used can return  (system users/ history / join requests
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
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
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
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
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
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
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
                        'users': system.get("users"),
                        'join_request': system.get("join_request"),
                    },
                    "success": True,
                }
            else:
                return {'message': "User does not have access","success": False,}
        else:
            return {'message': "System does not exist","success": False,}
    else:
        return {'message': "User does not exist","success": False,}

    



def register_system(request, dbClient):
    data = request.get_json()
    systemID = data['systemID']
    system_collection = dbClient.Systems.System
    system = system_collection.find_one({'systemID': systemID})
    if system is not None:
        data_arr = system.get("data_packets")
        for probe_data in data['probes']:
        # (1) Initialize a new probe entry
            probe_entry = {
            "date": datetime.today(),
            "probes": [],  # List to store probe data
            "tank_level": data.get('tank_level'),
        }

        # (2) Iterate over each attribute (light, moisture, temp) in the current probe data
        for key, value in probe_data.items():
            probe_entry["probes"].append({
                key: value
            })

        # (3) Append the probe entry to the data_arr
        data_arr.append(probe_entry)

    # (4) Update the MongoDB collection with the updated data_arr
        system_collection.update_one({"systemID": systemID}, {'$set': {'data_packets': data_arr}})
        return {'message': "Data Stored",}
    else:
        return {'message': "ERROR",}

