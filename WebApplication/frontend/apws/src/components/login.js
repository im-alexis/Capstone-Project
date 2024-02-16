import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";




class Login extends React.Component {
  constructor(props){
    super(props)
    this.login = this.login.bind(this)
    this.passwordHandler = this.passwordHandler.bind(this)
    this.usernameHandler = this.usernameHandler.bind(this)
    this.state = {
      user: "",
      pass: "",
      success: false
    }
  }
  passwordHandler(){
    var newPass = document.getElementById("password").value
    this.setState({
      pass: newPass
    })
    

  }
  usernameHandler(){
    var newUser = document.getElementById("username").value
    this.setState({
      user: newUser
    })
  }
  login(){
      


  }

  render(){
    return (
      <div id = "back">
          <div id = "login">
            <br />
            <h1>APWS</h1>
            <br />
            <label>Username   </label>
            <input id="username" type='text' name='user' value={this.user} onChange={this.usernameHandler}></input>
            <br/><br/>
            <label>Password   </label>
            <input id="password" type='password' name='user' value={this.pass} onChange={this.passwordHandler}></input>
            <br/><br/>
            <button id='loginBtn'>Login</button>
            {/* <button onClick={this.test}>test</button> */}
            <br/><br/>
            <Link to={"/"}>Forgot Password</Link>
            <br/><br/>
            <Link to='/Create-User'>Create New Account</Link> <br />
          </div>
      </div>
    )
  }
  
}

export default Login;