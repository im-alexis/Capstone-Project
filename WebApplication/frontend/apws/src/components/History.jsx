import '../styles/History.css';
import React,{useState, useEffect} from 'react'
import { BrowserRouter as Link} from "react-router-dom";

function History(props){

    useEffect(() =>{
        getHistory();
      },[]);//empty array so this only runs when component initially mounts

    const [ID, setID] = useState(sessionStorage.getItem("SysID"))
    const [user, setUser] =useState(sessionStorage.getItem("User"))
    const [HistList, setHistList] = useState([])

    function backToDash(){
        sessionStorage.removeItem("SysID")
        window.location.replace("/Dashboard")
    }
    useEffect(() =>{
        getHistory();
      },[]);//empty array so this only runs when component initially mounts

    const getHistory = async () => {
        const response = await fetch("http://127.0.0.1:5000/history", {
          method: "POST",
          mode: "cors",
          headers: {
            "content-Type": "application/json",
          },
          body: JSON.stringify({
            username: user,
            systemID: ID,
          }),
        })
        const data = await response.json();

        console.log(data)

        const list = data["message"]["data_packets"].map((p) =>(
            [p["date"],
            p["battery_level"],
            p["probes"][0]["humidity"],
            p["probes"][0]["light"],
            p["probes"][0]["moisture"],
            p["probes"][0]["temp"],
            p["tank_level"],
            ]
          ));

        setHistList(p => list)

        //const list = data["message"]["data_packets"];
        console.log(list)
    
        // alert(data['message'])
      }

    return(
        <div className='HistoryPage'>
            <button onClick={backToDash}>Back to DashBoard</button>
            <ul className='Hist-list'>
          {HistList.map((plant, index) =>
            <li key={index}>
              <ValueSet date={plant[0]}
                    battery_level={plant[1]}
                    humidityL={plant[2]}
                    lightL={plant[3]}
                    moistL={plant[4]}
                    tempL={plant[5]}
                    tankL={plant[6]}/>
            </li>
          )}
        </ul>
        </div>
    )
}

function ValueSet(props){
    return(
        <div className='HistData'>
            <p className='His-text'>date: {props.date}  </p>
            <p className='His-text'>Battery Level: {props.battery_level}%  </p>
            <p className='His-text'>Moisture Level: {props.moistL}  </p>
            <p className='His-text'>Temperature Level: {props.tempL}  </p>
            <p className='His-text'>Humidity Level: {props.humidityL}  </p>
            <p className='His-text'>Light level: {props.lightL}</p>
            <p className='His-text'>Tank level: {props.tankL}</p>
        </div>
    )
}

export default History