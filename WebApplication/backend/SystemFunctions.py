#AWPS: Backend
# Home of System Infomation Display:
#   1) /dashboard (Return the most reacent data_packet of each systemt the user is part of)
#   2) /history (Return a specific system's data array )
#   3) /system - Might be obselete but if used can return  (system users/ history / join requests
#   4) /system_users - (Returns the array of users(w/ thier role) of a given system)
#   5) /notifications


# /dashboard
    #Request format
#     {
#      "username": username,
#      "systemID": someID,
# }

# /history
    #Request format
#     {
#      "username": username,
#      "systemID": someID,
# }

#AWPS: Backend
# Home of System Infomation Display:
#   1) /dashboard
#   2) /history
#   3) /system
#   4) /system_users
#   5) /notifications

from bson import ObjectId
from datetime import datetime


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

