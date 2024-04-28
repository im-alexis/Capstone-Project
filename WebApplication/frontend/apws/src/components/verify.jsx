import { useEffect } from 'react';
import React, { useState } from 'react'
import "../styles/verify.css";
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";

function Verify () {
  const [user, setUser] = useState(sessionStorage.getItem('user'));
  const [otp, setOtp] = useState("")
  const [success, setSuccess] = useState(false)
  const [type, setType] = useState("")

  useEffect(() => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const data = urlParams.get('data');
    setType(data);
  }, []);

  const otpHandler = (event) => {
    setOtp(event.target.value);
  };

  const verify = async () => {
    const response = await fetch("http://127.0.0.1:5000/verify", {
        method: 'POST',
        mode: "cors",
        headers:{
            'content-Type':'application/json'
        },
        body: JSON.stringify({
          username: user,
          OTP: otp,
        })
    })
    const data = await response.json();
    // console.log(data)
    setSuccess(data["access"]);

    if (data["access"] === true) {
      window.alert("OTP Approved")
      if(type === "fp") {window.location.replace(`/reset_password`)}
      else {
        sessionStorage.clear();
        window.location.replace(`/Login`)
      }
    } 
    else {alert("Incorrect Code");}
  }

  return (
    <div id = "back">
        <div id = "verify">
          <br />
          <h1>OTP Verification</h1>
          <input type="otp" id="otp" maxLength="6" value={otp} onChange={otpHandler} required></input>
          <br/><br/>
          <button onClick={verify} id='vbutton'>Continue</button> 
          <br/><br/>
          <Link to='/'>Back To Sign In</Link> <br />
      </div>
    </div>
  )

}

export default Verify