from pymongo import MongoClient
import sys
sys.path.insert(0, '/Users/alexistorres/Documents/Code/Capstone-Project/WebApplication/backend')
import cypher

client = MongoClient(
    "mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")
systems_db = client.Systems
users_db = client.Users
user_collection = users_db.User
system_collection = users_db.Systems


newUser = {
            "username": "alexistorres@utexas.edu",
            "password": cypher.encrypt("password"),
            "systems": [],
        }
user_collection.insert_one(newUser)


