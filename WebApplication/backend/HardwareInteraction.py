#AWPS: Backend
# Home of Operations that interact with HW:
#   1) /update_settings
#   2) /water
#   3) /data
#   3) /GetInstructions
from datetime import datetime
'''
For route /update_settings

    Request format
    {
     "username": username,
     "systemID": someID,
     "settings" : [moister_min, sample_rate]
    } 

'''
def sys_update_settings(request, dbClient):
    data = request.get_json()
    username = data['username'].lower()
    systemID = data['systemID']
    setting_arry = data['settings']

    if any (entry < 1 for entry in setting_arry ):
        return{'message': "Values less than one are not allowed"}
    
    user_collection = dbClient.Users.User
    user = user_collection.find_one({"username": username}, {"systems": 1})
    if user is None:
        return{'message': username + " does not exist"}
    
    system_collection = dbClient.Systems.System
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
/GetInstructions?systemID=somevalue
  
'''

def get_instructions_hw(systemID, dbClient):
    system_collection = dbClient.Systems.System
    system = system_collection.find_one({'systemID': systemID})
    if system is None:
        return [-1,-1,-1]
    else:
        settings = system.get("settings", []) # is an array of integers [waterTime (In msec), MoistRange (0 to 100), SampleTime(in mins)]
        #return {'message': settings}
        return settings