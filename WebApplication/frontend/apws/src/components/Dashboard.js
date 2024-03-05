import React from 'react'
import "../styles/dashboard.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";
import Plant from './Plant';




function Dashboard(){

  return(
    <div>
      <header>
        <h1>APWS</h1>
        <a href='/'>
        <button>Sign Out</button>
        </a>
        <button>Settings</button> 
      </header>
      <div>
        <Plant></Plant>
      </div>
      <footer>
        <p>&copy; APWS {new Date().getFullYear}</p>
      </footer>
    </div>
  );

}

  
export default Dashboard;