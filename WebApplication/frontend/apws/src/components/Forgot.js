import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

class Forgot extends React.Component {
    constructor(props){
      super(props)
      this.forgot = this.forgot.bind(this)
      this.emailHandler = this.emailHandler.bind(this)
      this.state = {
        email: "",    // NOTE SHOULD USERNAMES JUST BE EMAILS??
        success: false
      }
    }

    emailHandler(){
      var newEmail = document.getElementById("email").value
      this.setState({
        email: newEmail
      })
    }

    forgot(){}
  
    render(){
      return (
        <div id = "back">
            <div id = "login">
              <br />
              <h1>APWS</h1>
              <br/>
              <label>Email   </label>
              <input type='email' name='user' value={this.email} id='email'></input>
              <br/><br/>
              <button  id='loginBtn'>Forgot Password</button> 
              <br/><br/>
              <Link to='/'>Sign in</Link> <br />
          </div>
        </div>
      )
    }
  }
  
  export default Forgot;