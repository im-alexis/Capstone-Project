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

# For route /register_system
    #Request format
#     {
#      "username": username,
#      "systemID": someID,
# }
def register_system(request, dbClient):
    data = request.get_json()
    username = data['username']
    username.lower()
    systemID = data['systemID']
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    user = user_collection.find_one({"username": username})
    system = system_collection.find_one({'systemID': systemID})
    if system is None:
        newSystem = {
            "systemID": systemID,
            "users": [{
                  "userID": user.get('_id'),
                  "username": username,
                  "access_level": 0,
            },],
            "data_packets": [],
            "join_request": [],
        }
        id_item = system_collection.insert_one(newSystem).inserted_id
        sys_array = user.get("systems")
        sys_array.append({
            "mongoID": id_item,
            "systemID":systemID,
            "access_level": 0,
        })
        user_collection.update_one({"username":username},{'$set':{'systems':sys_array}})
        return {'message': "System registered",}
    else:
        return {'message': "System already registered",}



# For route /data
    #Request format
#     {
#      "systemID": someID,
#      "tank_level": someValue
#      "probes": [
#           {
#              "moisture" : someValue,
#              "temp" : someValue,
#              "light" : someValue,
#               "humidity" : someValue,
#           }, ...
#      ],
# }
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
    
# For route /change_role

    #Request format
#     {
#      "username": username,
#      "systemID": someID,
#      "target": usernameTarget,
#      "action": (
    #Action 0: Change to Owner
    #Action 1: Change to Admin
    #Action 2: Change to Reg
    #Action 3: Remove from System:  Owner -> Admin/Reg | Admin -> Reg | Reg -> None
#    )    
# } 
def change_role(request, dbClient):
    #Action 0: Change to Owner
    #Action 1: Change to Admin
    #Action 2: Change to Reg
    #Action 3: Remove from System:  Owner -> Admin/Reg | Admin -> Reg | Reg -> None

    return "TEST"


# For route /join_system_request  
    #Request format
#     {
#      "username": username,
#      "systemID_target": someID,   
# } 
def join_system_request(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID_target']
    user_collection = dbClient.Users.User
    system_collection = dbClient.Systems.System
    user = user_collection.find_one({"username": username})
    system = system_collection.find_one({'systemID': systemID})
    
    if system is not None:
        system_user_arry = system.get("users")
        join_req_arr = system.get("join_request")
       
        for entry in system_user_arry:
            if entry["username"].lower() == username:
                return {'message': "You are already a memeber",}
            
        for obj in join_req_arr:
            if obj["username"].lower() == username:
                return {'message': "Request exist",}

        join_req_arr.append({
                "date": datetime.today(),
                "user": user,
        })
        system_collection.update_one({"systemID":systemID},{'$set':{'join_request':join_req_arr}})
        return {'message': "Request has been sent",}
    else:
        return {'message': "System does not exist",}
            



