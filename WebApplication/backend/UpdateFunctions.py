#AWPS: Backend
# Home of Operations that Update Items:
#   1) /update_settings
#   2) /change_role
#   3) /leave_system
#   4) /join_system
#   5) /akn_request
#   6) /register_system
#   7) /data


def register_system(request, dbClient):
    username = request.form['username']
    systemID = request.form['systemID']
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
    else:
        return {'message': "System already registered"}
    return {'message': "System registered"}
