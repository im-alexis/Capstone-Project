import random
from pymongo import MongoClient

client = MongoClient("mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")
username = "kietle24@utexas.edu"
user_collection = client.Users.User
user = user_collection.find_one({'username': username})
while user:
    OTP = random.randint(1000, 9999)
    if user_collection.find_one({'OTP': OTP}) is False:
        break
update = {"$set": {"OTP": OTP}}
remove = {"$unset": {"OTP": ""}}
user_collection.update_one(user, remove)