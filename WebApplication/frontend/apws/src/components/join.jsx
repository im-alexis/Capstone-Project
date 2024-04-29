import '../styles/join.css';
import React, { useState } from "react";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";


function Join(props){
    const [user, setUSer] = useState(sessionStorage.getItem("User"));
    const [ID, setID] = useState("");

    function handleSetID(event){
        setID(event.target.value);

    }
    const joinPlant = async () => {
        const response = await fetch("http://127.0.0.1:5000/join_system_request", {
          method: "POST",
          mode: "cors",
          headers: {
            "content-Type": "application/json",
          },
          body: JSON.stringify({
            username: user,
            systemID_target: ID,
          }),
        })
        const data = await response.json();
    
        alert(data['message'])
      }


    return(
        <div className='JoinPage'>
            <div id="join">
                <br />
                <h1 id="joinHead">APWS</h1>
                <br />
                <label id="IDLabel">System ID</label>
                <input id="SystemID" type="text" name="SystemID" value={ID} onChange={handleSetID} placeholder='eg. abc123' required ></input>
                <br /><br />
                <button id='registerSystemBtn' onClick={joinPlant}>Join Plant</button>
                <br /><br />
                <Link to="/Dashboard" id='jlink'>Back to DashBoard</Link> <br />
            </div>
        </div>
    )
}


export default Join