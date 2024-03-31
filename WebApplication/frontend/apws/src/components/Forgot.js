import React from 'react'
import "../styles/forgot.css";
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

    forgot(){
      fetch("http://127.0.0.1:5000/forgot_password", {
        method: 'POST',
        mode: "cors",
        headers:{
          'content-Type':'application/json'
        },
        body: JSON.stringify({
          username: this.state.user,
        })
      })
      
      .then(response => response.json())
      .then((data) => {
        this.setState({
          success: data['access'],
        })
      })
      setTimeout(() => {
        if(this.state.success === true){
          window.alert("Reset Code Sent")
          // window.location.replace(`/reset_password`)  /* Not Created Yet */
        }else{
          window.alert("User No Existing User")
          alert("User Does Not Exist")
        }
      }, 500); // 2000 milliseconds = 2 seconds
        
    }
  
    render(){
      return (
        <div id = "back">
            <div id = "fp">
              <br />
              <h1>APWS</h1>
              <label>Email   </label>
              <input type='email' name='user' value={this.email} id='email'></input>
              <br/><br/>
              <button onClick={this.forgot} id='FPBtn'>Forgot Password</button> 
              <br/><br/>
              <Link to='/'>Back To Sign In</Link> <br />
          </div>
        </div>
      )
    }
  }
  
  export default Forgot;