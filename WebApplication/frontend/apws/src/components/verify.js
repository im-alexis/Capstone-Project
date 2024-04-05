import React from 'react'
import "../styles/verify.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

class Verify extends React.Component {
    constructor(props){
      super(props)
      this.verify = this.verify.bind(this)
      this.emailHandler = this.emailHandler.bind(this)
      var queryString = window.location.search
      var urlParams = new URLSearchParams(queryString)
      var data = urlParams.get('data')
      this.state = {
        email: "",
        success: false,
        type: data,
      }
    }

    emailHandler(){
      var newEmail = document.getElementById("email").value
      this.setState({
        email: newEmail
      })
    }

    verify(){
      fetch("http://127.0.0.1:5000/verify", {
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
            window.alert("OTP Approved")
            if(this.state.type === "fp") {window.location.replace(`/reset_password`)}
            else {window.location.replace(`/dashboard`)}
        }else{
          window.alert("Incorrect Code")
          alert("Incorrect Code")
        }
      }, 500); // 2000 milliseconds = 2 seconds
        
    }
  
    render(){
      return (
        <div id = "back">
            <div id = "verify">
              <br />
              <h1>OTP Verification</h1>
              <br/><br/>
              <input type="otp" id="otp" maxlength="6"></input>
              <br/><br/>
              <button onClick={this.verify} id='FPBtn'>Continue</button> 
              <br/><br/>
              <Link to='/'>Back To Sign In</Link> <br />
          </div>
        </div>
      )
    }
  }
  
  export default Verify;