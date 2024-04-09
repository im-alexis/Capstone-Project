import React from 'react'
import "../styles/forgot.css";
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
        console.log(data['access'])
        this.setState({
          success: data['access'],
        })
      })
      setTimeout(() => {
        if(this.state.success === true){
          window.alert("Reset Code Sent")
          sessionStorage.setItem('user', this.state.user) // IDK what this might do (trying to transfer data b/w pages)
          window.location.replace(`/verify?data=` + encodeURIComponent("fp"))
        }else{
          window.alert("User No Existing User")
        }
      }, 1000); // 2000 milliseconds = 2 seconds
        
    }
  
    render(){
      return (
        <div id = "back">
            <div id = "fp">
              <br />
              <h1>APWS</h1>
              <label>Email   </label>
              <input type='email' name='user' value={this.user} onChange={this.usernameHandler} required id='username'></input>
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