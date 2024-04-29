import plantpic from '../styles/plantpic.jpg';
import '../styles/Plant.css';
import PropTypes from 'prop-types';
import { BrowserRouter as Routes, Route, useNavigate, Link, Navigate} from "react-router-dom";
import Plant_Settings from './settings';



function Plant(props){

    const plantSettings = () => {
        sessionStorage.setItem('SysID', props.sysID)
        window.location.replace('/Plant_Settings')
    }
    function toHistory(){
        sessionStorage.setItem('SysID', props.sysID)
        window.location.replace('/plantHistory')
    }

    return(
        <div className='plantCard'>
            <img className='img' src={plantpic} ></img>
            <h2 className='card-title'>{props.name}</h2>
            <p className='card-text'>Moisture Level: {props.moistL}  </p>
            <p className='card-text'>Temperature Level : {props.tempL}  </p>
            <p className='card-text'>Humidity Level: {props.humidityL}  </p>
            <p className='card-text'>Light Level: {props.lightL}</p>
            <p className='card-text'>Water Level: {props.tankL}</p>
            <p className='card-text'>Battery: {props.batL}</p>
            <p className='card-text'>SystemID: {props.sysID}</p>
            <p className='card-text'>Alerts : {props.alerts}</p>
            <button className='history-btn' onClick={toHistory}>History</button>
            <br></br>
            <button className='plant-settings-btn' onClick={plantSettings}>plant settings</button>
            <br></br>
        </div>
    )
}

Plant.propTypes = {
    name: PropTypes.string,
    moistL: PropTypes.number,
    tempL: PropTypes.number,
    humidL: PropTypes.number,
    lightL: PropTypes.number,
    alerts: PropTypes.string,
}

Plant.defaultProps = {
    name: "Plant Name",
    moistL: "n/a",
    tempL: "n/a",
    humidL: "n/a",
    lightL: "n/a",
    alerts: "n/a",

}

export default Plant