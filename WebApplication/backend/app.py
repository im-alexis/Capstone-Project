#AWPS: Backend
# Home of Routes

from flask import Flask, request, session
from pymongo import MongoClient
from flask_cors import CORS
import SystemInformation, UpdateFunctions, LoginFunctions, InviteHandler, HardwareInteraction

#LOOK INTO SESSIONS
app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://alexistorres1802:PsVRgNszt317idtn@apws.qpzzxgw.mongodb.net/")

# ^var resposnse is in JSON formatting
# ^Function can be compressed to be send in the request

# 
#login route
@app.route("/", methods=['POST'])
def login_page():
    response = LoginFunctions.sign_in(request,client)
    print(response)
    return response

#create_user route
@app.route("/create_user", methods=['POST'])
def create_user():
    print(request.get_json())
    response = LoginFunctions.sign_up(request,client)
    print(response)
    return response  # This is a Json Response

#forgot password route
@app.route("/forgot_password", methods=['POST'])
def forgot_password():
    response = LoginFunctions.forgot_request(request,client)
    return response

#OTP Check
@app.route("/verify", methods=['POST'])
def verify():
    response = LoginFunctions.otp_verify(request,client)
    return response

#reset password
@app.route("/reset", methods=['POST'])
def reset():
    response = LoginFunctions.reset_password(request,client)
    return response


#register_system route
@app.route("/register_system", methods=['POST'])
def register_system():
    response = ''
    response = UpdateFunctions.register_system(request, client)
    return response

#/change_role route
@app.route("/change_role", methods=['POST'])
def change_role():
    response = UpdateFunctions.change_role(request,client)
    return response

#dashboard route
@app.route("/dashboard", methods=['POST'])
def dashboard():
    response = ''
    return "Placeholder"

#system route
@app.route("/system", methods=['POST'])
def system():
    response = SystemInformation.sys_info(request, client)
    return response

# ! Could just /system as it sends every parameter

#/history route
@app.route("/history", methods=['POST'])
def history():
    response = SystemInformation.get_history(request,client)
    return response

#notifications route
@app.route("/notifications", methods=['POST'])
def notifications():
    return "Placeholder"

#/system_users route
@app.route("/system_users", methods=['POST'])
def system_users():
    response = SystemInformation.get_sys_users(request,client)
    return response

# ! Could just /system as it sends every parameter



#system_invite route
@app.route("/system_invite", methods=['POST'])
def system_invite():
    response = InviteHandler.sys_user_invite(request,client)
    return response

@app.route("/sys_invite_akn", methods=['POST'])
def sys_invite_akn():
    response = InviteHandler.user_akn_invite(request,client)
    return response
#leave_system route
@app.route("/leave_system", methods=['POST'])
def leave_system():
    response = ''
    response = InviteHandler.leave_sys(request, client)
    return response

#join_system route
@app.route("/join_system_request", methods=['POST'])
def join_system():
    response = InviteHandler.join_system_request(request, client)
    return response

#akn_request route
@app.route("/akn_request", methods=['POST'])
def akn_request():
    response = InviteHandler.akn_join_request(request,client)
    return response
#update_settings route
@app.route("/update_settings", methods=['POST'])
def update_settings():
    #TBD Not sure how settings will look like
    response = HardwareInteraction.sys_update_settings(request, client)
    return response

#water route
@app.route("/water", methods=['POST'])
def water():
    response = HardwareInteraction.water_plant(request,client)
    return response

#data route
@app.route("/data", methods=['POST'])
def data():
    response = HardwareInteraction.recieve_data_packet(request,client)
    return response

#Route for HW to recive intructions
@app.route("/GetInstructions", methods=['GET'])
def GetInstructions():
    sysID = request.args.get('systemID')
    response = HardwareInteraction.get_instructions_hw(sysID,client)
    return response


if __name__ == "__main__":
    app.run(debug=True,host = '0.0.0.0')