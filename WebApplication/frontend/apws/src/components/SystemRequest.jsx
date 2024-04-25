import React,{useState, useEffect} from 'react'
import "../styles/dashboard.css";
import JoinRequest from './JoinRequest';

function SystemRequest () {
  const [user, setUSer] = useState(sessionStorage.getItem("User"));
  const [requestList, setRequest] = useState([]);

  const loadRequests = async () => {
    const response = await fetch("http://127.0.0.1:5000/system", {
      method: "POST",
      mode: "cors",
      headers: {
        "content-Type": "application/json",
      },
      body: JSON.stringify({
        username: user,
      }),
    })
    const data = await response.json();
  }

  return(
    <div className='requestPage'>
      <header className='dash-head'>
        <h1 className='dash-title'>APWS</h1> 
      </header>
      <div className='dash-display'>
        <ul className='request-list'>
          {requestList.map((plant, index) =>
            <li key={index}>
              <JoinRequest name={plant[0]}
                      humidityL={plant[1]}
                      lightL={plant[2]}
                      moistL={plant[3]}
                      tempL={plant[4]}
                      tankL={plant[5]}
                      sysID={plant[6]}
                      alerts={plant[7]} />
            </li>
          )}
        </ul>
      </div>
      <footer className='dash-foot'>
        <p className='copyright'>&copy; APWS {new Date().getFullYear()}</p>
      </footer>
    </div>
  );

}

export default SystemRequest