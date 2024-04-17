from pymongo import MongoClient

#Was going line by line to see what shows up at the variable
dbClient = MongoClient("mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")
system_collection = dbClient.APWS.Systems

system = system_collection.find_one({'systemID': 'some-identification'})
authorized_users = system['users']

user_collection = dbClient.APWS.Users
user = user_collection.find_one({"username": "alexistorres@utexas.edu"})

item_id = user.get("_id")
sys_array = user.get("systems")
sys_array.append({
            "systemID":'some-identification',
            "mongoID": system.get('_id'),
            "access_level": 0,
        })
user_collection.update_one({"username": "alexistorres@utexas.edu"},{'$set':{'systems':sys_array}})
print(authorized_users[0])