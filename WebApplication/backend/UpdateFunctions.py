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
For route /change_role

    Request format
    {
     "username": username,
     "systemID": someID,
     "target": usernameTarget,
     "action": (
    Action 0: Change to Owner(0) -> Not doing ATM
    Action 1: Change to Admin(1)
    Action 2: Change to Reg (2)
    Action 3: Remove from System:  Owner -> Admin/Reg | Admin -> Reg | Reg -> None
        )    
    } 
'''
def change_role(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    target = data['target'].lower()
    action = data['action']
    system_collection = dbClient.Systems.System
    user_collection = dbClient.Users.User

    # Check if the user making the request exists
    user = user_collection.find_one({'username': username}, {'systems': 1})
    if user is None:
        return {'message': "There is no user logged in"}

    # Check if the system exists
    system = system_collection.find_one({'systemID': systemID}, {'users': 1})
    if system is None:
        return {'message': "System does not exist"}

    # Check if the target user exists
    target_obj = user_collection.find_one({'username': target}, {'systems': 1})
    if target_obj is None:
        return {'message': "The user does not exist"}

    user_sys_arr = user.get("systems", [])
    sys_user_arr = system.get("users", [])
    tar_sys_arr = target_obj.get("systems", [])

    # Check if the target user is in the system
    if not any(entry['username'] == target for entry in sys_user_arr):
        return {'message': "User is not in the System"}

    # Check if the target user is associated with the system
    if not any(entry['systemID'] == systemID for entry in tar_sys_arr):
        return {'message': "User is not in the System"}

    if action == 1 or action == 2:
        # Update access level for both user and target
        for entry in user_sys_arr:
            if entry['systemID'] == systemID and entry['access_level'] == 0:
                for user_entry in sys_user_arr:
                    if user_entry['username'] == target:
                        user_entry['access_level'] = action
                for target_entry in tar_sys_arr:
                    if target_entry['systemID'] == systemID:
                        target_entry['access_level'] = action
                system_collection.update_one({"systemID": systemID}, {'$set': {'users': sys_user_arr}})
                user_collection.update_one({"username": target}, {'$set': {'systems': tar_sys_arr}})
                return {'message': target + ' role updated to ' + str(action)}
        return {'message': 'Action is only allowed by owner'}

    elif action == 3:
        # Remove user from the system
        for entry in user_sys_arr:
            if entry['systemID'] == systemID:
                if entry['access_level'] == 0:
                    for e in sys_user_arr[:]:  # Using slicing to create a copy of sys_user_arr
                        if e['username'] == target:
                            sys_user_arr.remove(e)
                    for e in tar_sys_arr[:]:  # Using slicing to create a copy of tar_sys_arr
                        if e['systemID'] == systemID and e['access_level'] < 1:
                            tar_sys_arr.remove(e)
                            user_collection.update_one({"username": target}, {'$set': {'systems': tar_sys_arr}})
                            return {'message': target + ' was removed'}
                    return {'message': target + ' is not able to be removed'}
                elif entry['access_level'] == 1:
                    for e in tar_sys_arr[:]:  # Using slicing to create a copy of tar_sys_arr
                        if e['systemID'] == systemID and e['access_level'] == 2:
                            tar_sys_arr.remove(e)
                    for e in sys_user_arr[:]:  # Using slicing to create a copy of sys_user_arr
                        if e['username'] == target and e['access_level'] == 2:
                            sys_user_arr.remove(e)
                    system_collection.update_one({"systemID": systemID}, {'$set': {'users': sys_user_arr}})
                    user_collection.update_one({"username": target}, {'$set': {'systems': tar_sys_arr}})
                    return {'message': target + ' was removed'}
                else:
                    return {'message': 'Only Admin+ is allowed to remove users'}
        return {'message': 'Invalid Action'}

    else:
        return {'message': 'Invalid Action'}





