import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

class dashboard extends React.Component {
    constructor(props){
      super(props)
      this.dashboard = this.dashboard.bind(this)
      this.emailHandler = this.emailHandler.bind(this)
      this.state = {
        email: "", 
        success: false
      }
    }

    emailHandler(){
      var newEmail = document.getElementById("email").value
      this.setState({
        email: newEmail
      })
    }

    dashboard(){}
  
    render(){
        return (
          <div id = "back">
              <div id = "login">
                <br />
                <h1>APWS</h1>
                <br/>
                <br />
            </div>
          </div>
        )
      }
    }
  
  export default dashboard;