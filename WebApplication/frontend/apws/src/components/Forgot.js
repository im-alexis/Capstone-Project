import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

class Forgot extends React.Component {
    constructor(props){
      super(props)
      this.forgot = this.forgot.bind(this)
      this.usernameHandler = this.usernameHandler.bind(this)
      this.state = {
        user: "",
        success: false
      }
    }

    usernameHandler(){
      var newUser = document.getElementById("username").value
      this.setState({
        user: newUser
      })
    }

    forgot(){
      fetch("API URL", {
        method: ("API METHOD"),
        mode: "cors",
        headers:{
          'content-Type':'application/json'
        },
        body: JSON.stringify({
          Username: this.state.user,
        })
      })
      
      .then(response => response.json())
      .then((data) => {
        this.setState({
          success: data['Access'],
          user: data['Username']
        })
      })
        
  
  
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