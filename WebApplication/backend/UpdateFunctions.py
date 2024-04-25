#AWPS: Backend
# Home of Operations that Update Items:
#   1) /change_role (Changing the role of user )
#   2) /register_system (Introduce a new system into the database )
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
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    system = system_collection.find_one({'systemID': system_id})
    user = user_collection.find_one({'username': username})
    if user is None:
        return {'message': 'User does not exist'}
    if system is None:
        new_system = {
            "systemID": system_id,
            "sys_name": "System-" +str(system_id), 
            "users": [{
                "username": username,
                "access_level": 2,     # Registering System = Owner of System 
            }],
            "data_packets": [],
            "join_request": [],
            "notifications": [],
            "settings": [0,12000,10, 5],
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
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

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

'''
For route /rename_sys

    Request format
    {
     "username": username,
     "systemID": someID,
     "new_name": some_name,
    } 
    only admin plus
'''

def update_sys_name(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    new_name = data['new_name']

    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    # Check if the user making the request exists
    user = user_collection.find_one({'username': username}, {'systems': 1})
    if user is None:
        u_sys_arr = user.get("systems", [])
        flg = False
        for e in u_sys_arr:
            if e['systemID'] == systemID:
                flg = True
                if e['access_level'] > 1:
                    return {'message' : 'User cannot update system name'}
        if not flg:
            return {'message': username + ' is not part of the system'}

    # Check if the system exists
    system = system_collection.find_one({'systemID': systemID}, {'users': 1})
    if system is None:
        return {'message': "System does not exist"}
    
    system_collection.update_one({"systemID": systemID}, {'$set': {'sys_name': new_name}})

    return{"message": "System custom name has been updated to "+ new_name}
