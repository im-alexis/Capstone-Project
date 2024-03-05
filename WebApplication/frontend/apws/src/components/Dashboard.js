import React from 'react'
import "../styles/dashboard.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";
import Plant from './Plant';





function Dashboard(){

  return(
    <div className='dashboard'>
      <header className='dash-head'>
        <h1 className='dash-title'>APWS</h1>
        <button className='head-btn'>Sign Out</button>
        <button className='head-btn'>Settings</button> 
      </header>
      <div className='dash-display'>
        <button id='joinBtn'>Join</button>
        <div>
          <Plant></Plant>
          <Plant></Plant>
          <Plant></Plant>
          <Plant></Plant>
        </div> 
        
      </div>
      <footer className='dash-foot'>
        <p>&copy; APWS {new Date().getFullYear()}</p>
      </footer>
    </div>
  );

}



// class Dashboard extends React.Component {
//     constructor(props){
//       super(props)
//       this.Dashboard = this.Dashboard.bind(this)

//       this.state = {
//         email: "", 
//         success: false
//       }
//     }

//     // emailHandler(){
//     //   var newEmail = document.getElementById("email").value
//     //   this.setState({
//     //     email: newEmail
//     //   })
//     // }

//     Dashboard(){}
  
//     render(){
//         return (
//           <div>
//         </div>
//         )
//       }
//     }
  
export default Dashboard;