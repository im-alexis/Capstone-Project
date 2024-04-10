import random
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText

# client = MongoClient("mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")
# username = "kietle24@utexas.edu"
# user_collection = client.Users.User
# user = user_collection.find_one({'username': username})
# OTP = 0000
# while user_exists(username, client):
#     temp = random.randint(1000, 9999)
#     if user_collection.find_one({'OTP': OTP}) is None:
#         OTP = temp
#         break
# print(OTP)  
# update = {"$set": {"OTP": OTP}}
# # remove = {"$unset": {"OTP": ""}}
# user_collection.update_one(user, update)

