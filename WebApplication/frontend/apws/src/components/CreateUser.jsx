import React from 'react'
import { useState } from "react";
import "../styles/CreateUser.css";
import { BrowserRouter as Routes, Route, useNavigate, Link} from "react-router-dom";

function CreateUser () {
  const [user, setUser] = useState("")
  const [pass, setPass] = useState("")
  const [pass2, setPass2] = useState("")
  const [success, setSuccess] = useState(false)

  const usernameHandler = (event) => {
    setUser(event.target.value)
  }

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

  const signUp = async() => {
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
                                       
      const response = await fetch("http://127.0.0.1:5000/create_user", {
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
        sessionStorage.setItem('user', user)
        window.location.replace(`/verify`)
      } 
      else {window.alert('Error');}   
  }
  return (
    <div id = "back">
      <div id = "cu">
        <h1>APWS</h1>
        <label id ='cuu'>Username   </label>
        <input type='text' name='user' value={user} id='username' onChange={usernameHandler}></input>
        <br/><br/>
        <label id ='cup'>Password</label>
        <input type='password' name='user' value={pass} id='pass1' onChange={passwordHandler} ></input>
        <br/><br/>
        <label id ='curp'>Re-enter Password</label>
        <input className='passLbl' type='password' name='user' id='pass2' onChange={passwordHandler2}></input>
        <br/><br/>
        <p>PASSWORD MUST CONTAIN:</p>
        <p>- at least 6 charachters</p>
        <p>- at least 1 number and letter</p>
        <p>- cannot contain "!" or " "</p>
        <br/><br/>
        <button onClick={signUp} id='loginBtn'>Create Account</button>  
        <br/><br/>
        <div id = "links">
          <Link to='/Login'>Back To Sign In</Link>
          <br />
        </div>
      </div>

    </div>
  )
}

export default CreateUser