from pymongo import MongoClient
from datetime import datetime
#test if snippit of code can put data packet in database
dbClient = MongoClient(
    "mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")

data = {
        "systemID": "test123", 
        "tank_level":42.5, 
        "probes":[
                {"light": 40,
                 "moisture": 30,
                 "temp": 35},
                {"light": 20,
                 "moisture": 35,
                 "temp": 25}
                ],
                }
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
