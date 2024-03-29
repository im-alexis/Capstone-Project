#AWPS: Backend
# Home of Operations that Update Items:
#   1) /update_settings
#   2) /change_role (Changing the role of user )
#   3) /leave_system (User leaves a system, not the Owner )
#   4) /join_system_request (User sends an Join request to a system )
#   5) /akn_request (From Owner/Admin perspective: accept/deny join request)
#   6) /register_system (Introduce a new system into the database )
#   7) /data
from datetime import datetime

'''
For route /register_system
    Request format
    {
     "username": username,
     "systemID": someID,
}
'''
def register_system(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    system_id = data['systemID']
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
    system = system_collection.find_one({'systemID': system_id})
    user = user_collection.find_one({'username': username})
    if user is None:
        return {'message': 'User does not exist'}
    if system is None:
        new_system = {
            "systemID": system_id,
            "users": [{
                "username": username,
                "access_level": 0,
            }],
            "data_packets": [],
            "join_request": [],
            "notifications": [],
        }
        system_collection.insert_one(new_system)
        
        user = user_collection.find_one({"username": username})
        if user:
            user_systems = user.get("systems", [])
            user_systems.append({
                "systemID": system_id,
                "access_level": 0,
            })
            user_collection.update_one({"username": username}, {'$set': {'systems': user_systems}})
        
        return {'message': "System registered"}
    else:
        return {'message': "System already registered"}



'''
For route /data
    Request format
    {
     "systemID": someID,
     "tank_level": someValue
     "probes": [
          {
             "moisture" : someValue,
             "temp" : someValue,
             "light" : someValue,
              "humidity" : someValue,
          }, ...
     ],
}
'''
def recieve_data_packet(request, dbClient):
    data = request.get_json()
    systemID = data['systemID']
    system_collection = dbClient.Systems.System
    system = system_collection.find_one({'systemID': systemID})
    if system is not None:
        data_arr = system.get("data_packets")
        data_arr.append({
            "date": datetime.today(),
            "probes": data['probes'],
            "tank_level": data['tank_level'],
        })
        system_collection.update_one({"systemID":systemID},{'$set':{'data_packets':data_arr}})
        return {'message': "Data Stored",}
    else:
        return {'message': "ERROR",}
    
'''
For route /akn_request
    Request format
    {
     "systemID": someID,
     "target": usernameTarget,
     "action": (
    Action 0: Deny
    Action 1: Allow
   )   
}
'''
    
def akn_join_request(request, dbClient):
    data = request.get_json()
    action = data['action']
    target = data['target'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
    system = system_collection.find_one({'systemID': systemID})
    if system is None:
        return {'message': "System does not exist"}

    system_user_arry = system.get("users", [])
    join_req_arr = system.get("join_request", [])
    
    userTarget = user_collection.find_one({"username": target})
    if userTarget is None:
        return {'message': "User does not exist"}

    user_sys_arr = userTarget.get("systems", [])

    if any(entry["username"].lower() == target for entry in system_user_arry):
        return {'message': "User is already a member"}
    
    join_req_user = next((entry for entry in join_req_arr if entry["username"].lower() == target), None)
    if join_req_user:
        join_req_arr.remove(join_req_user)
        if action == 1:
            # ALLOW
            system_user_arry.append({"username": target, "access_level": 2})
            user_sys_arr.append({"systemID": systemID, "access_level": 2})
            system_collection.update_one({"systemID": systemID}, {'$set': {'users': system_user_arry, 'join_request': join_req_arr}})
            user_collection.update_one({"username": target}, {'$set': {'systems': user_sys_arr}})
            return {'message': "User has been added"}
        else:
            # DENY
            system_collection.update_one({"systemID": systemID}, {'$set': {'join_request': join_req_arr}})
            return {'message': "User request denied"}
    
    # Invite does not exist
    return {'message': "Invite does not exist"}



'''
For route /change_role

    Request format
    {
     "username": username,
     "systemID": someID,
     "target": usernameTarget,
     "action": (
    Action 0: Change to Owner(0)
    Action 1: Change to Admin(1)
    Action 2: Change to Reg (2)
    Action 3: Remove from System:  Owner -> Admin/Reg | Admin -> Reg | Reg -> None
        )    
    } 
'''
def change_role(request, dbClient):
    #Action 0: Change to Owner
    #Action 1: Change to Admin
    #Action 2: Change to Reg
    #Action 3: Remove from System:  Owner ->Admin/Reg | Admin -> Reg | Reg -> None
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    target_user = data['target'].lower()
    action = data['action']
    system_collection = dbClient.Systems.System
    user_collection = dbClient.Users.User

    return "TEST"

'''
For route /join_system_request  
    Request format
    {
     "username": username,
     "systemID_target": someID,   
} 
'''
def join_system_request(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    system_id = data['systemID_target']
    
    system_collection = dbClient.Systems.System
    system = system_collection.find_one({'systemID': system_id}, {'users': 1, 'join_request': 1})
    
    if system:
        system_users = system.get("users", [])
        join_requests = system.get("join_request", [])
        
        for user_entry in system_users:
            if user_entry["username"].lower() == username:
                return {'message': "You are already a member"}
        
        for req_entry in join_requests:
            if req_entry["username"].lower() == username:
                return {'message': "Request already exists"}
        
        join_requests.append({
            "date": datetime.today(),
            "username": username,
        })
        
        system_collection.update_one({'systemID': system_id}, {'$set': {'join_request': join_requests}})
        return {'message': "Request has been sent"}
    else:
        return {'message': "System does not exist"}


'''
For route /leave_system

    Request format
    {
     "username": username,
     "systemID": someID,
     
    } 
'''


def leave_sys(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    system_id = data['systemID']
    
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    
    user = user_collection.find_one({'username': username}, {'systems': 1})
    system = system_collection.find_one({'systemID': system_id}, {'users': 1})
    
    if user:
        user_systems = user.get("systems", [])
        if system:
            system_users = system.get("users", [])
            for user_entry in system_users:
                if user_entry["username"].lower() == username:
                    if user_entry["access_level"] == 0:
                        return {'message': 'Owner cannot leave a system'}
                    else:
                        system_collection.update_one({'systemID': system_id},
                                                     {'$pull': {'users': {'username': username}}})
                        user_collection.update_one({'username': username},
                                                   {'$pull': {'systems': {'systemID': system_id}}})
                        return {'message': f"{username} has left system: {system_id}"}
            return {'message': f"{username} is not a member of {system_id}"}
        else:
            return {'message': f"{system_id} does not exist"}
    else:
        return {'message': f"{username} does not exist"}



