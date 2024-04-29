import '../styles/Register.css';
import React, { useState } from "react";
import PropTypes from 'prop-types';
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";


function Register(props){
    const [user, setUSer] = useState(sessionStorage.getItem("User"));
    const [ID, setID] = useState("");
    const [height, setHeight] = useState("");

    function handleSetID(event){
        setID(event.target.value);

    }
    function handleSetHeight(event){
      setHeight(event.target.value);

  }
    const registerPlant = async () => {
        const response = await fetch("http://127.0.0.1:5000/register_system", {
          method: "POST",
          mode: "cors",
          headers: {
            "content-Type": "application/json",
          },
          body: JSON.stringify({
            username: user,
            systemID: ID,
            tank_size: height,
          }),
        })
        const data = await response.json();
    
        alert(data['message'])
      }


    return(
        <div className='RegisterPage'>
            <div id="register">
                <br />
                <h1 id='regHead'>APWS</h1>
                <br />
                <label id="rIDLabel">System ID</label>
                <input id="rSystemID" type="text" name="SystemID" value={ID} onChange={handleSetID} placeholder='eg. abc123' required ></input>
                <br /><br />
                <label id="HeightLabel">Tank Height(cm)</label>
                <input id="TankHeight" type="text" name="TankHeight" value={height} onChange={handleSetHeight} placeholder='eg. 20' required ></input>
                <br /><br />
                <button id='regSystemBtn' onClick={registerPlant}>Register Plant</button>
                <br /><br />
                <Link to="/Dashboard" id='rlink'>Back to DashBoard</Link> <br />
            </div>
        </div>
    )
}

Register.propTypes = {

}

Register.defaultProps = {

}

export default Register