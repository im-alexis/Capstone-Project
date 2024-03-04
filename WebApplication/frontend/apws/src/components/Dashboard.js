import React from 'react'
import "../styles/dashboard.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

class Dashboard extends React.Component {
    constructor(props){
      super(props)
      this.Dashboard = this.Dashboard.bind(this)

      this.state = {
        email: "", 
        success: false
      }
    }

    // emailHandler(){
    //   var newEmail = document.getElementById("email").value
    //   this.setState({
    //     email: newEmail
    //   })
    // }

    Dashboard(){}
  
    render(){
        return (
          <div>
        </div>
        )
      }
    }
  
  export default Dashboard;