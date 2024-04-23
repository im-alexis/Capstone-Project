import React, { useState } from "react";
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate } from "react-router-dom";

function Login() {
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [success, setSuccess] = useState(false);

  const passwordHandler = (event) => {
    setPass(event.target.value);
  };

  const usernameHandler = (event) => {
    setUser(event.target.value);
  };

  const login = async () => {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      mode: "cors",
      headers: {
        "content-Type": "application/json",
      },
      body: JSON.stringify({
        username: user,
        password: pass,
      }),
    })
    const data = await response.json();
    setSuccess(data["access"]);

    if (data["access"] === true) {
      sessionStorage.setItem("User",user)
      window.location.replace('/Dashboard');
    } 
    else {
      alert(data['message']);
    }
  }

  return (
  <div id="back">
    <div id="login">
      <br />
      <h1>APWS</h1>
      <br />
      <label id="emailLabel">Email </label>
      <input id="username" type="email" name="user" value={user} onChange={usernameHandler} required></input>
      <br /><br />
      <label id="passwordLabel">Password </label>
      <input id="password" type="password" name="user" value={pass} onChange={passwordHandler} required></input>
      <br /><br />
      <button onClick={login} id="loginBtn"> Login </button>
      {/* <button onClick={test}>test</button> */}
      <br /><br />
      <Link to="/Forgot">Forgot Password</Link>
      <br /><br />
      <Link to="/Create-User">Create New Account</Link> <br />
    </div>
  </div>
  );
}

export default Login;
