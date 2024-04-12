import React from "react";
import "../styles/login.css";
import {
  BrowserRouter as Routes,
  Route,
  useNavigate,
  Link,
  Navigate,
} from "react-router-dom";

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.login = this.login.bind(this);
    this.passwordHandler = this.passwordHandler.bind(this);
    this.usernameHandler = this.usernameHandler.bind(this);
    this.state = {
      user: "",
      pass: "",
      success: false,
    };
  }

  passwordHandler() {
    var newPass = document.getElementById("password").value;
    this.setState({
      pass: newPass,
    });
  }

  usernameHandler() {
    var newUser = document.getElementById("username").value;
    this.setState({
      user: newUser,
    });
  }

  login() {
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      mode: "cors",
      headers: {
        "content-Type": "application/json",
      },
      body: JSON.stringify({
        username: this.state.user,
        password: this.state.pass,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          success: data["access"],
        });
      });
    setTimeout(() => {
      if (this.state.success === true) {
        window.location.replace(`/Dashboard`);
      } else {
        alert("Incorrect Username or Password");
      }
    }, 500); // 2000 milliseconds = 2 seconds
  }

  render() {
    return (
      <div id="back">
        <div id="login">
          <br />
          <h1>APWS</h1>
          <br />
          <label id="emailLabel">Email </label>
          <input
            id="username"
            type="email"
            name="user"
            value={this.user}
            onChange={this.usernameHandler}
            required
          ></input>
          <br />
          <br />
          <label id="passwordLabel">Password </label>
          <input
            id="password"
            type="password"
            name="user"
            value={this.pass}
            onChange={this.passwordHandler}
            required
          ></input>
          <br />
          <br />
          <button onClick={this.login} id="loginBtn">
            Login
          </button>
          {/* <button onClick={this.test}>test</button> */}
          <br />
          <br />
          <Link to="/Forgot">Forgot Password</Link>
          <br />
          <br />
          <Link to="/Create-User">Create New Account</Link> <br />
        </div>
      </div>
    );
  }
}

export default Login;
