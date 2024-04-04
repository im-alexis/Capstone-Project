#AWPS: Backend
# Home of Routes

from flask import Flask, request, session
from pymongo import MongoClient
from flask_cors import CORS
import SystemInformation, UpdateFunctions, LoginFunctions, InviteHandler

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
    response = ''
    response = LoginFunctions.sign_in(request,client)

    #     data = request.get_json()
    # print(data)
    # if 'Username' in data and data['Username'] != "":
    #     response = {"Username" : data["Username"], "Access" : True}
    #     return response
    
    # global username_global
    # username_global = username
    return response

#create_user route
@app.route("/create_user", methods=['POST'])
def create_user():
    # print("REACHED")
    # print(request)
    # print(client)
    response = ''
    response = LoginFunctions.sign_up(request,client)
    print(response)
    # global username_global
    # username_global = username
    # session['username'] = Username
    return response  # This is a Json Response

   

#forgot password route
@app.route("/forgot_password", methods=['POST'])
def forgot_password():
    response = LoginFunctions.forgot_request(request,client)
    return response

#OTP Check
@app.route("/verify", methods=['POST'])
def forgot_password():
    response = LoginFunctions.otp_verify(request,client)
    return response

#reset password
@app.route("/reset", methods=['POST'])
def forgot_password():
    response = LoginFunctions.reset_password(request,client)
    return response

#dashboard route
@app.route("/dashboard", methods=['POST'])
def dashboard():
    response = ''
    return "Placeholder"

#register_system route
@app.route("/register_system", methods=['POST'])
def register_system():
    response = ''
    response = UpdateFunctions.register_system(request, client)
    return response

#system route
@app.route("/system", methods=['POST'])
def system():
    response = SystemInformation.sys_info(request, client)
    return response

#update_settings route
@app.route("/update_settings", methods=['POST'])
def update_settings():
    #TBD Not sure how settings will look like
    response = ''
    return "Placeholder"
# ! Could just /system as it sends every parameter
#/history route
@app.route("/history", methods=['POST'])
def history():
    response = ''

    return "Placeholder"

#notifications route
@app.route("/notifications", methods=['POST'])
def notifications():
    return "Placeholder"

#/system_users route
@app.route("/system_users", methods=['POST'])
def system_users():
    response = ''
    return "Placeholder"
# ! Could just /system as it sends every parameter
#/change_role route
@app.route("/change_role", methods=['POST'])
def change_role():
    response = UpdateFunctions.change_role(request,client)
    return response

#system_invite route
@app.route("/system_invite", methods=['POST'])
def system_invite():
    return "Placeholder"

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


#Route for Hardware, TBD if ardino nano can do post requests
#data route
@app.route("/data", methods=['POST'])
def data():
    response = UpdateFunctions.recieve_data_packet(request,client)
    return response


if __name__ == "__main__":
    app.run(debug=True,host = '0.0.0.0')