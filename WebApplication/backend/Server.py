#AWPS: Backend
# Home of Routes

from flask import Flask, request, session
import SystemFunctions, UpdateFunctions, LoginFunctions

#LOOK INTO SESSIONS
app = Flask(__name__)

#var resposnse is in JSON formatting

#login route
@app.route("/", methods=['POST'])
def login_page():
    response = ''
    username = request.form['username']
    password = request.form['password']
    response = LoginFunctions.sign_in(username, password)
    # global username_global
    # username_global = username
    return response

#create_user route
@app.route("/create_user", methods=['POST'])
def create_user():
    response = ''
    username = request.form['username']
    password = request.form['password']
    response = LoginFunctions.sign_up( username, password)
    # global username_global
    # username_global = username
    # session['username'] = Username
    return response  # This is a Json Response

   

#forgot_password route
@app.route("/forgot_password", methods=['POST'])
def forgot_password():
    response = ''
    username = request.form['username']
    response = LoginFunctions.password_reset(username)
    return response

#dashboard route
@app.route("/dashboard", methods=['POST'])
def dashboard():
    return "Placeholder"

#register_system route
@app.route("/register_system", methods=['POST'])
def register_system():
    return "Placeholder"

#system route
@app.route("/system", methods=['POST'])
def system():
    return "Placeholder"

#update_settings route
@app.route("/update_settings", methods=['POST'])
def update_settings():
    return "Placeholder"

#history route
@app.route("/history", methods=['POST'])
def history():
    return "Placeholder"

#system_users route
@app.route("/system_users", methods=['POST'])
def system_users():
    return "Placeholder"

#change_role route
@app.route("/change_role", methods=['POST'])
def change_role():
    return "Placeholder"

#system_invite route
@app.route("/system_invite", methods=['POST'])
def system_invite():
    return "Placeholder"

#leave_system route
@app.route("/leave_system", methods=['POST'])
def leave_system():
    return "Placeholder"

#notifications route
@app.route("/notifications", methods=['POST'])
def notifications():
    return "Placeholder"

#join_system route
@app.route("/join_system", methods=['POST'])
def join_system():
    return "Placeholder"

#akn_request route
@app.route("/akn_request", methods=['POST'])
def akn_request():
    return "Placeholder"


#Route for Hardware, TBD if ardino nano can do post requests
#data route
@app.route("/data", methods=['POST'])
def data():
    return "Placeholder"


if __name__ == "__main__":
    app.run(debug=True)