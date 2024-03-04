import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link} from "react-router-dom";
class CreateUser extends React.Component {
  constructor(props){
    super(props)
    this.signUp = this.signUp.bind(this)
    this.passwordHandler = this.passwordHandler.bind(this)
    this.usernameHandler = this.usernameHandler.bind(this)
    this.state = {
      user: "",
      pass: "",
      pass2: "",
      success: false
    }
  }
  passwordHandler(){
    var newPass = document.getElementById("pass1").value
    this.setState({
      pass: newPass
    })
  }
  
  usernameHandler(){
    var newUser = document.getElementById("username").value
    this.setState({
      user: newUser
    })
  }

  Valid(txt){

    if(txt.length < 6){
      return false
    }
    var hasNumber = false
    for (var i=0; i <txt.length; i++){
      console.log(txt[i])
      console.log(isNaN(txt[i]))
      if(!isNaN(txt[i])){
        hasNumber = true
        
      }
      if(txt[i] === '!' || txt[i] === ' '){
        return false
      }
    }
    console.log(hasNumber)
    if(hasNumber === false){
      return false
    }
    else{
      return true
    }
  }

  signUp(){
    let pass1 = document.getElementById("pass1").value
    let pass2 = document.getElementById("pass2").value
    let user = document.getElementById("username").value
    let uValid = this.Valid(user)
    let pValid = this.Valid(pass1)

    if(!uValid){
      window.alert("Username not valid")
      return
    }
    if(pass1 !== pass2){
      window.alert("Passwords do not match")
      return
    }
    if(!pValid){
      window.alert("password not valid")
      return
    }
    
    this.usernameHandler()
    this.passwordHandler()

    fetch("http://127.0.0.1:5000/create_user", {
      method: 'POST',
      mode: "cors",
      headers:{
        'content-Type':'application/json'
      },
      body: JSON.stringify({
        Username: this.state.user,
        Password: this.state.pass
      })
    })
    
    .then(response => response.json())
    .then((data) => {
      this.setState({
        success: data['Access'],
      })
    })
    
    setTimeout(() => {
      if(this.state.success === true){
        window.alert("successfully Created")
        window.location.replace(`/`)
      }else{
        window.alert("Username already exists")
      }
    }, 500); // 2000 milliseconds = 2 seconds

  }

  render(){
    return (
      <div id = "back">
  
        <div id = "login">
          <h1>APWS</h1>
          <label>Username   </label>
          <input type='text' name='user' value={this.user} id='username'></input>
          <br/><br/>
          <label>Password</label>
          <input type='password' name='user' value={this.pass} id='pass1' ></input>
          <br/><br/>
          <label className='passLbl'>Re-enter Password</label>
          <input className='passLbl' type='password' name='user' id='pass2'></input>
          <p>password and username must contain:</p>
          <p>*atleast 6 charachters</p>
          <p>*atleast 1 number and letter</p>
          <p>*cannot contain "!" or " "</p>
          <button  id='loginBtn'>Create Account</button> 
          <br/><br/>
          <Link to='/'>Sign in</Link> <br />
        </div>
  
      </div>
    )
  }
  
}

export default CreateUser;