#AWPS: Backend
# Home of Routes

from flask import Flask, request, session
from flask_cors import CORS

#LOOK INTO SESSIONS
app = Flask(__name__)
CORS(app)


#login route
@app.route("/", methods=['POST'])
def login_page():
    data = request.get_json()
    print(data)
    if 'Username' in data and data['Username'] != "":
        response = {"Username" : data["Username"], "Access" : True}
        return response
    return "Placeholder"

#create_user route
@app.route("/create_user", methods=['POST'])
def create_user():
    return "Placeholder"

#forgot_password route
@app.route("/forgot_password", methods=['POST'])
def forgot_password():
    return "Placeholder"

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