import React,{useState, useEffect} from 'react'
import "../styles/dashboard.css";
import Plant from './Plant';

function Dashboard(){
  //might need to use  useRef instead of useState if rendering problems occur with useEffect
  const[plants, setPlants] = useState([["plant 1" , 0, 1, 2, 3, 4], ["plant 2" , 0, 11, 22, 33, 44]]);

  useEffect(() =>{
    //this is the fetch from create user, will uncomment and make necceesarry changes once backend is complete
    // fetch("http://127.0.0.1:5000/create_user", {
    //     method: 'POST',
    //     mode: "cors",
    //     headers:{
    //       'content-Type':'application/json'
    //     },
    //     body: JSON.stringify({
    //       username: u,
    //       password: p,
    //     })
    //   })
    
    //   .then(response => response.json())
    //   .then((data) => {
    //     console.log("What's going on")
    //     console.log(data['message'])
    //     if (data['message'] === 'User added.') {
    //       this.setState({
    //         success: true,
    //       })}
    //   })
  },[]);//empty array so this only runs when component initially mounts

  function add_plant(){
      const newPlant = ["plant" , 0, 11, 22, 33, 44]
      setPlants(p => [...p, newPlant])
  }

  return(
    <div className='dashboard'>
      <header className='dash-head'>
        <h1 className='dash-title'>APWS</h1>
        <a href='/'>
          <button className='head-btn'>Sign Out</button>
        </a> 
        <button className='head-btn'>Settings</button>
      </header>
      <div className='dash-display'>
        <button className='joinBtn' onClick={add_plant}>Join</button>
        <ul className='plant-list'>
          {plants.map((plant, index) =>
            <li key={index}>
              <Plant name={plant[0]}
                      moistL={plant[1]}
                      tempL={plant[2]}
                      humidL={plant[3]}
                      lightL={plant[4]}
                      alerts={plant[5]} />
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

  
export default Dashboard;