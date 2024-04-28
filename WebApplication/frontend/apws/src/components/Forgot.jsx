import React, { useState } from 'react'
import "../styles/forgot.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

function Forgot() {
    const [user, setUser] = useState("");
    const [success, setSuccess] = useState(false);

    const usernameHandler = (event) => {
        setUser(event.target.value);
    };

    const forgot = async () => {
        const response = await fetch("http://127.0.0.1:5000/forgot_password", {
            method: 'POST',
            mode: "cors",
            headers:{
                'content-Type':'application/json'
            },
            body: JSON.stringify({
                username: user,
            })
        })

        const data = await response.json();
        // console.log(data)
        setSuccess(data["access"]);

        if (data["access"] === true) {
            window.alert("Reset Code Sent")
            sessionStorage.setItem('user', user) // transfer data b/w pages
            window.location.replace(`/verify?data=` + encodeURIComponent("fp"))
        } 
        else {
            alert("User No Existing User");
        }
    }

    return (
    <div id = "back">
        <div id = "fp">
            <br />
            <h1>APWS</h1>
            <label id="fplabel">Email   </label>
            <input type='email' name='user' value={user} onChange={usernameHandler} required id='fpinput'></input>
            <br/><br/>
            <button onClick={forgot} id='fpbutton'>Forgot Password</button> 
            <br/><br/>
            <Link to='/Login'>Back To Sign In</Link> <br />
        </div>
    </div>
    )
}

export default Forgot;