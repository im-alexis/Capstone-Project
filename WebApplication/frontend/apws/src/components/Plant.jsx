import plantpic from '../styles/plantpic.jpg';
import '../styles/Plant.css';
import PropTypes from 'prop-types';


function Plant(props){


    return(
        <div className='plantCard'>
            <img className='img' src={plantpic} ></img>
            <h2 className='card-title'>{props.name}</h2>
            <p className='card-text'>Moisture Level: {props.moistL}  </p>
            <p className='card-text'>Temperature Level: {props.tempL}  </p>
            <p className='card-text'>Humidity Level: {props.humidL}  </p>
            <p className='card-text'>Light level: {props.lightL}</p>
            <p className='card-text'>Alerts : {props.alerts}</p>
            <button className='history-btn' >History</button>
            <br></br>
            <button className='plant-settings-btn'>plant settings</button>
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