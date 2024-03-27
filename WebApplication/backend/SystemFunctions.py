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