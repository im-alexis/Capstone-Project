#AWPS: Backend
# Home of Operations that Deal With Inviting:
#   2) /change_role (Changing the role of user )
#   3) /leave_system (User leaves a system, not the Owner )
#   4) /join_system_request (User sends an Join request to a system )
#   5) /akn_request (From Owner/Admin perspective: accept/deny join request)
#   6) /system_invite

from datetime import datetime
import MessageFunctions

'''
For route /akn_request
    Request format
    {
    "username" : someUserName
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
    username = data['username'].lower()
    action = data['action']
    target = data['target'].lower()
    systemID = data['systemID']
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    user = user_collection.find_one({"username": username})
    if user:
        u_sys_arr = user.get("systems", [])
        flg = False
        for e in u_sys_arr:
            if e['systemID'] == systemID:
                flg = True
                if e['access_level'] > 1:
                    return {'message' : 'User cannot akn join request'}
                
        if not flg:
            return {'message': username + ' is not part of the system'}
        
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

    system_collection = dbClient.APWS.Systems
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
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems
    
    user = user_collection.find_one({'username': username}, {'systems': 1})
    system = system_collection.find_one({'systemID': system_id}, {'users': 1})
    
    if user:
        if system:
            system_users = system.get("users", [])
            for user_entry in system_users:
                if user_entry["username"].lower() == username:
                    if user_entry["access_level"] == 0:
                        return {'message': 'Owner cannot leave a system',}
                    else:
                        system_collection.update_one({'systemID': system_id},
                                                     {'$pull': {'users': {'username': username}}})
                        user_collection.update_one({'username': username},
                                                   {'$pull': {'systems': {'systemID': system_id}}})
                        return {'message': f"{username} has left system: {system_id}",}
            return {'message': f"{username} is not a member of {system_id}",}
        else:
            return {'message': f"{system_id} does not exist",}
    else:
        return {'message': f"{username} does not exist",}


'''
For route /system_invite
    An admin sends an invite to a user
    Request format
    {
     "username": username,
     "systemID": someID,
     "target": target_username,
    } 

'''
# Only an Admin and Above can send a invite to a user
def sys_user_invite(request, dbClient):
    data = request.get_json() # Unpack Request
    username = data['username'].lower()
    systemID = data['systemID']
    target_user = data['target'].lower()

    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    user = user_collection.find_one({"username": username})
    # Initial check of existance of the user and the system
    if not user:
        return {'message': username + ' does not exist',}
    system = system_collection.find_one({'systemID': systemID })

    if not system:
        return {'message': "System does not exist"}

    user_systems = {sys['systemID']: sys['access_level'] for sys in user.get('systems', [])}
    if systemID not in user_systems:
        return {'message': 'User is not part of system',}

    if user_systems[systemID] > 1: # Validate the user can send the invite to a user
        return {'message': 'User cannot send an invite to other users',}

    user_target = user_collection.find_one({"username": target_user})
    if not user_target:
        return {'message': "User Target does not exist"}

    invites = user_target.get("sys_invites", [])
    if any(invite['systemID'] == systemID for invite in invites):
        return {'message': 'Invite already exists',}
    
    systems = user_target.get("systems", [])
    if any(sys['systemID'] == systemID for sys in systems):
        return {'message': 'User already a memeber of system',}

    invites.append({
        "date": datetime.today(),
        "systemID": systemID,
    })

    user_collection.update_one({'username': target_user}, {'$set': {'sys_invites': invites}})
    
    # Send an email notification
    MessageFunctions.send_email(subject="System Invite", systemID=systemID, case=6, recipient=target_user, user=username)
    
    return {'message': "Invite has been sent",}



'''
For route /sys_invite_akn
    An admin sends an invite to a user
    Request format
    {
     "username": username,
     "systemID": someID,
     "action": 1 {Accept}, 0 {Reject}
    } 

'''
def user_akn_invite(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    action = data['action']
    
    if action not in [0, 1]:
        return {"message": "Action is invalid"}
    
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    user = user_collection.find_one({"username": username})
    if not user:
        return {'message': username + ' does not exist',}
    sys_list = user.get("systems", [])
    
    system = system_collection.find_one({"systemID": systemID})
    if not system:
        return {'message': systemID + ' does not exist',}
    
    invites = user.get("sys_invites", [])
    
    invite = next((entry for entry in invites if entry["systemID"] == systemID), None)
    if invite:
        if action == 1:
            system_user_arry = system.get("users", [])
            system_user_arry.append({
                'username':username,
                'access_level': 2
            })
            system_collection.update_one({"systemID": systemID}, {'$set': {'users': system_user_arry}})
            invites.remove(invite)
            sys_list.append({
                "systemID": systemID,
                "access_level": 2
            })
            user_collection.update_one({"username": username}, {'$set': {'sys_invites': invites, 'systems': sys_list}})
            return {"message" : "Invite accepted, successfully added"}
        elif action == 0:
            invites.remove(invite)
            user_collection.update_one({"username": username}, {'$set': {'sys_invites': invites, 'systems': sys_list}})
            return {"message" : "Invite rejected"}
    else:
        return {'message': "Invite does not exist"}
    

