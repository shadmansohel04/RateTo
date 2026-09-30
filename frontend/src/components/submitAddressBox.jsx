import '../styles/submitAddressBox.css'
import arrow from '../assets/arrow.png';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function SubmitAddressComponent(){
    const [address, setAddress] = useState("") 
    const navigate = useNavigate()

    function clickHandler(){
        if(address.length == 0){
            return
        }
        let newArray = address.split(" ")
        newArray = newArray.map((each, index) => {
            if(index != newArray.length-1){
                return each + "+"
            }
            else{
                return each
            }
        })
        let formattedAddress = newArray.join("");

        navigate("/map/" + formattedAddress)
    }

    function handleKeyDown(event){
        if(event.key == "Enter"){
            clickHandler()
        }
    }

    return(
        <div className="submitAddressBox">
            <h1 className='logo'>RateTO</h1>
            <h2>Discover Toronto in a whole new way</h2>
            <div className='inputTo'>
                <input onKeyDown={handleKeyDown} type="text" name="addresss" id="address" placeholder='Enter address here' onChange={(event) =>{setAddress(event.target.value)}}/>
                <button onClick={clickHandler}><img src={arrow} alt="arrow" /></button>
            </div>
            <a href="https://www.instagram.com/souvenirpixels/">Picture by James Wheeler</a>
        </div>
    )
}