from flask import Flask, request, session

#LOOK INTO SESSIONS
app = Flask(__name__)


#login page
@app.route("/", methods=['POST'])
def login_page():
    return "Placeholder"




if __name__ == "__main__":
    app.run(debug=True)