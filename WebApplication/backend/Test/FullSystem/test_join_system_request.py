from pymongo import MongoClient

dbClient = MongoClient(
    "mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")

def join_system_request(request):
    username = request['username'].lower()
    systemID = request['systemID_target']
    system_collection = dbClient.Systems.System
    system = system_collection.find_one({'systemID': systemID})
    
    if system is not None:
        system_user_arry = system.get("users")
        join_req_arr = system.get("join_request")
       
        for entry in system_user_arry:
            if entry["username"].lower() == username:
                return {'message': "You are already a memeber",}
        for obj in join_req_arr:
            if obj["username"].lower() == username:
                return {'message': "Request exist",}

        # join_req_arr.append({
        #         "date": datetime.today(),
        #         "user": user,
        # })
        # system_collection.update_one({"systemID":systemID},{'$set':{'join_request':join_req_arr}})
        return {'message': "Request has been sent",}
    else:
        return {'message': "System does not exist",}
    

def test_request_going_thru():
     #This Request Should be sent thru
    request1 = {
        "username": "kietle24@utexas.edu",
        "systemID_target" : "test123"
    }
    response = join_system_request(request1)
    assert response["message"] ==  "Request has been sent"

def test_existing_system_member():
    #This Request should be denyed , due being in the system already 
    request2 = {
        "username": "alexistorres@utexas.edu",
        "systemID_target" : "test123"
    }
    response = join_system_request(request2)
    assert response["message"] ==  "You are already a memeber"

def test_request_exist():
    #This request should be denyed, request exist
    request3 = {
    "username": "someOneJoining",
    "systemID_target" : "test123"
    }
    response = join_system_request(request3)
    assert response["message"] ==  "Request exist"

def test_system_DNE():
    request3 = {
    "username": "alexistorres@utexas.edu",
    "systemID_target" : "systemDoesNotExist"
    }
    response = join_system_request(request3)
    assert response["message"] ==  "System does not exist"

