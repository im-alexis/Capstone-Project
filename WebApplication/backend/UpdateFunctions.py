#AWPS: Backend
# Home of Operations that Update Items:
#   1) /update_settings
#   2) /change_role
#   3) /leave_system
#   4) /join_system
#   5) /akn_request
#   6) /register_system
#   7) /data
from datetime import datetime

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