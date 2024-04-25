#AWPS: Backend
# Home of Operations that interact with HW:
#   1) /update_settings
#   2) /water
#   3) /data
#   3) /GetInstructions
from datetime import datetime
'''
For route /update_settings

    delayTime, moistureCutoff, pumpActiveLength, and pumpOnTime
    Request format
    {
     "username": username,
     "systemID": someID,
     "settings" : [moistureCutoff, delayTime ,pumpActiveLength ]
    } 
    Settings Array in Mongo [pumpOnTime (in secs), moistureCutoff (idk), delayTime (in mins), pumpActiveLength (in secs)t5]
'''
def sys_update_settings(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    setting_arry = data['settings']

    if any (entry < 1 for entry in setting_arry ):
        return{'message': "Values less than one are not allowed"}
    
    user_collection = dbClient.APWS.Users
    user = user_collection.find_one({"username": username}, {"systems": 1})
    if user is None:
        return{'message': username + " does not exist"}
    
    system_collection = dbClient.APWS.Systems
    system = system_collection.find_one({'systemID': systemID})
    if system is None:
        return {'message': systemID + " does not exist" }
    
    for entry in user.get('systems', []):
        if entry['systemID'] == systemID:
            if entry['access_level'] > 1:
                return {'message': 'User cannot update settings'}
            break
    else:
        return {'message': f"{username} is not part of the system {systemID}"}
    
    settings = system.get('settings', [])
    settings[1] = setting_arry[0]
    settings[2] = setting_arry[1]
    settings[3] = setting_arry[2]
    system_collection.update_one({"systemID": systemID}, {'$set': {'settings': settings}})

    return {'message': "Settings have been updated"}
   
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
    system_collection = dbClient.APWS.Systems
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
/GetInstructions?systemID=somevalue
  Settings Array in Mongo [pumpOnTime (in secs), moistureCutoff (idk), delayTime (in mins), pumpActiveLength (in secs) ]
'''

def get_instructions_hw(systemID, dbClient):
    system_collection = dbClient.APWS.Systems
    system = system_collection.find_one({'systemID': systemID})
    if system is None:
        return {"delayTime":-1,"moistureCutoff":-1,"pumpOnSeconds":-1,"pumpActiveLength" : -1}
    else:
        settings = system.get("settings", []) 
        #return {'message': settings}
        time_pump = settings[0]
        settings[0] = 0 
        system_collection.update_one({"systemID": systemID}, {'$set': {'settings': settings}})
        return {"delayTime":settings[2],"moistureCutoff":settings[1],"pumpOnSeconds":time_pump,"pumpActiveLength" : settings[3]} #{in Minutes, IDK Range, in seconds}
    
'''
For route /water

    Request format
    {
     "username": username,
     "systemID": someID,
     "amount": someValue,
    } 
'''

def water_plant(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    amount = data["amount"]
    if amount < 0:
        return {"message": "You crazy!! No negative numbers"}
    if amount > 30:
        return {"message": "I soft limit you to 30secs"} 
    user_collection = dbClient.APWS.Users
    system_collection = dbClient.APWS.Systems

    # Combine queries to get user and system information in a single query
    user_system = user_collection.find_one({"username": username, "systems.systemID": systemID})

    if user_system is None:
        return {'message': f"{username} does not exist or is not part of the system {systemID}"}

    # Check access level
    for entry in user_system.get('systems', []):
        if entry['systemID'] == systemID:
            if entry['access_level'] > 1:
                return {'message': 'User cannot trigger manual water'}
            break
    else:
        return {'message': f"{username} is not part of the system {systemID}"}

    # Increment water sec count
    system_collection.update_one({"systemID": systemID}, {'$inc': {'settings.0': amount}})

    return {'message': "Water Ping has been queued"}