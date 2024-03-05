import plantpic from '../styles/plantpic.jpg';
import '../styles/Plant.css';


function Plant(){

    return(
        <div className='plantCard'>
            <img className='img' src={plantpic} ></img>
            <h2 className='card-title'>Plant Name</h2>
            <p className='card-text'>Moisture Level: n/a  </p>
            <p className='card-text'>Temperature Level: n/a  </p>
            <p className='card-text'>Humidity Level: n/a  </p>
            <p className='card-text'>Light level: n/a</p>
            <p className='card-text'>Alerts : n/a</p>
            <button className='history-btn' >History</button>
            <br></br>
            <button className='plant-settings-btn'>plant settings</button>
        </div>
    )
}
export default Plant