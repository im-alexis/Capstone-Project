import React, { useState } from 'react'
import "../styles/reset_password.css";
import { BrowserRouter as Routes, Route, useNavigate, Link} from "react-router-dom";

function Reset_password () {
  const [user, setUser] = useState(sessionStorage.getItem('user'))
  const [pass, setPass] = useState("")
  const [pass2, setPass2] = useState("")
  const [success, setSuccess] = useState(false)

  const passwordHandler = (event) => {
    setPass(event.target.value);
  };

  const passwordHandler2 = (event) => {
    setPass2(event.target.value);
  };

  const Valid = (txt) => {

    if(txt.length < 6){
      return false
    }
    let hasNumber = false
    for (let i=0; i <txt.length; i++){
      if(!isNaN(txt[i])){
        hasNumber = true
        
      }
      if(txt[i] === '!' || txt[i] === ' '){
        return false
      }
    } 
    // console.log(hasNumber)
    if(hasNumber === false){
      return false
    }
    else{
      return true
    }
  };

  const reset = async() => {
    let uValid = Valid(user)
    let pValid = Valid(pass)

    if(!uValid){
      window.alert("Username not valid")
      return
    }
    if(pass !== pass2){
      window.alert("Passwords do not match")
      return
    }
    if(!pValid){
      window.alert("password not valid")
      return
    }
                                       
      const response = await fetch("http://127.0.0.1:5000/reset", {
        method: 'POST',
        mode: "cors",
        headers:{
          'content-Type':'application/json'
        },
        body: JSON.stringify({
          username: user,
          password: pass,
        }),
      });

      const data = await response.json();

      if (data['access'] === true) {
        sessionStorage.clear();
        window.alert('Reset Password Successful');
        window.location.replace(`/Login`)
      } 
      else {window.alert('Error');}
  }

  return (
    <div id = "back">
      <div id = "rp">
        <h1>APWS</h1>
        <label id ='rpp'>New Password</label>
        <input type='password' name='user' value={pass} id='pass1' onChange={passwordHandler} ></input>
        <br/><br/>
        <label id ='rprp'>Re-enter Password</label>
        <input className='passLbl' type='password' name='user' id='pass2' onChange={passwordHandler2}></input>
        <br/><br/>
        <p>PASSWORD MUST CONTAIN:</p>
        <p>- at least 6 charachters</p>
        <p>- at least 1 number and letter</p>
        <p>- cannot contain "!" or " "</p>
        <br/><br/>
        <button onClick={reset} id='loginBtn'>Submit</button>  
        <br/><br/>
        <div id = "rplinks">
          <Link to='/Login'>Back To Sign In</Link>
          <br/>
        </div>
      </div>
    </div>
  )

}

export default Reset_password;