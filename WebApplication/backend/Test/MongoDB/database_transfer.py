from pymongo import MongoClient
dbClient = MongoClient(
    "mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")

old_sys_collection = dbClient.Systems.System
new_sys_collection = dbClient.APWS.Systems

old_usr_collection = dbClient.Users.User
new_usr_collection = dbClient.APWS.Users

cursor = old_sys_collection.find({})
for document in cursor:
    new_sys_collection.insert_one(document)

cursor = old_usr_collection.find({})
for document in cursor:
    new_usr_collection.insert_one(document)