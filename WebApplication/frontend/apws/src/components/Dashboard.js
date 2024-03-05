import React from 'react'
import "../styles/dashboard.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";
import Plant from './Plant';





function Dashboard(){

  return(
    <div className='dashboard'>
      <header className='dash-head'>
        <h1 className='dash-title'>APWS</h1>
        <a href='/'>
          <button className='head-btn'>Sign Out</button>
          <button className='head-btn'>Settings</button>
        </a> 
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

  
export default Dashboard;