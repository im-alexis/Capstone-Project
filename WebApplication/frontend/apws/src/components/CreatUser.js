import React from 'react'
import "../styles/login.css";
import { BrowserRouter as Routes, Route, useNavigate, Link} from "react-router-dom";
class CreateUser extends React.Component {
  constructor(props){
    super(props)
    this.signUp = this.signUp.bind(this)
    this.passwordHandler = this.passwordHandler.bind(this)
    // this.usernameHandler = this.usernameHandler.bind(this)
    this.state = {
      user: "",
      pass: "",
      pass2: "",
      success: false
    }
  }
  passwordHandler(newUser, newPass, callback){
    // var newPass = document.getElementById("pass1").value
    // console.log(newPass)
    this.setState({
      user: newUser,
      pass: newPass
    }, () => {
      // console.log(this.state.user);
      // console.log(this.state.pass);
      if (callback) {
        callback("Updated");
      }
    });
  }
  
  // usernameHandler(newUser){
  //   // var newUser = document.getElementById("username").value
  //   this.setState({
  //     user: newUser
  //   })
  // }

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

    console.log(user)
    console.log(pass1)
                                       
    // this.usernameHandler(user)
    this.passwordHandler(user, pass1, (updatedPass) => {
      // Perform actions that depend on the updated password here
      console.log(updatedPass);
      var u = this.state.user
      var p = this.state.pass
      console.log(u)
      console.log(p)
      fetch("http://127.0.0.1:5000/create_user", {
        method: 'POST',
        mode: "cors",
        headers:{
          'content-Type':'application/json'
        },
        body: JSON.stringify({
          username: u,
          password: p,
        })
      })
    
      .then(response => response.json())
      .then((data) => {
        console.log("What's going on")
        console.log(data['message'])
        if (data['message'] === 'User added.') {
          this.setState({
            success: true,
          })}
      })
      setTimeout(() => {
        if(this.state.success === true){
          window.alert("Successfully Created Account")
          window.location.replace(`/`)
        }else{
          console.log("What's going on 2")
          window.alert("Username already exists")
        }
      }, 500); // 2000 milliseconds = 2 seconds
    
    });

    // console.log(this.state.user)
    // console.log(this.state.pass)

    // fetch("http://127.0.0.1:8000/create_user", {
    //   method: 'POST',
    //   mode: "cors",
    //   headers:{
    //     'content-Type':'application/json'
    //   },
    //   body: JSON.stringify({
    //     Username: user,
    //     Password: pass1
    //   })
    // })
    
    // .then(response => response.json())
    // .then((data) => {
    //   console.log("What's going on")
    //   console.log(data['message'])
    //   if (data['message'] === 'User added.') {
    //     this.setState({
    //       success: true,
    //     })}
    // })
    
    // setTimeout(() => {
    //   if(this.state.success === true){
    //     window.alert("Successfully Created Account")
    //     window.location.replace(`/`)
    //   }else{
    //     console.log("What's going on 2")
    //     window.alert("Username already exists")
    //   }
    // }, 1000); // 2000 milliseconds = 2 seconds

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
          <button onClick={this.signUp} id='loginBtn'>Create Account</button>  
          <br/><br/>
          <Link to='/'>Sign in</Link> <br />
        </div>
  
      </div>
    )
  }
  
}

export default CreateUser;