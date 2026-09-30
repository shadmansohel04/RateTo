import { MapContainer, TileLayer, Marker, Popup, Polygon, Circle, Polyline } from 'react-leaflet';
import '../styles/map.css';
import 'leaflet/dist/leaflet.css';
import { useEffect, useMemo, useState, useRef } from 'react';
import axios from 'axios';
import loadingIMG from '../assets/loadingIMG.gif'
import {Hospitalclose, ttcIconMain, fireTruck, fireTruckBig, PoliceCar, PoliceCarClose, parkDesign, parkDesignClose, crimeDesign, circleDesign, Hospitals, ttcIcon, generic } from '../assets/markers';
import { useNavigate } from 'react-router-dom';
import img from "../assets/blueLine.png";
import green from "../assets/green.png"
import hood from "../assets/hood.png"

export default function MapComponent(props) {
    const navigate = useNavigate()
    const [color, setcolor] = useState("black")
    const [allMapData, setAllMapData] = useState()
    const [home, setHome] = useState()
    const [showHome, setShowHome] = useState("EMPTY")
    const [newAddress, setnewaddress] = useState('')
    const [address, setAddress] = useState(props.address)
    const [loading, setLoading] = useState(true)
    const [legendStyle, setLegend] = useState({
        width: '0vw',
        paddingleft: "0",
        paddingright: '0'
    })
    const [checked, setChecked] = useState({
        fire: true,
        hospital: true,
        police: true,
        ttc: true,
        bike: true,
        park: true,
        neighboorhood: true
    })
    const [scores, setScore] = useState()

    function inputAddress(event){
        setnewaddress(event.target.value)
    }

    function changeAddress(){
        setLoading(true)
        setcolor("white")
        setLegend({
            width: '0vw',
            paddingleft: "0",
            paddingright: '0'
        })
        setAddress(newAddress)
    }

    function handleCheck(event) {
        const { id, checked } = event.target;
        setChecked((prevChecked) => ({
            ...prevChecked,
            [id]: checked,
        }));
    }

    useEffect(() => {
        axios.get("https://rateto-backend.onrender.com/api/data", {
            params: {
                address: address,
                schoolChoice: "private"
            }
        }).then((response) => {
            if (response.data.success === true) {
                setAllMapData(response.data.data)
                setHome(response.data.data.home)
                setShowHome(response.data.data.homeAddress)
                setScore(response.data.data.scores)
                setcolor("black")
                setLoading(false)
            }
            else{
                alert("Please type valid Toronto Address")
                navigate("/")
            }
        });
    }, [address]);

    function onClickDrop(){
        const ismobile = window.innerWidth < 768;
        if (legendStyle.width == '0vw'){

            if(ismobile){
                setLegend({
                    width: "80vw",
                    paddingleft: "4%",
                    paddingright: "2%"
                })

            }

            else{
                setLegend({
                    width: "35vw",
                    paddingleft: "2%",
                    paddingright: "2%"
                })
            }

            setcolor("white")
        }

        else{
            setLegend({
                width: "0vw",
                paddingleft: "0",
                paddingright: "0"
            })
            setcolor("black")
        }    
    }

    function DraggableMarker(){
        const markerRef = useRef(null)
        const eventHandlers = useMemo(
            () => ({
              dragend() {
                const marker = markerRef.current
                if (marker != null) {
                    setLoading(true)
                    setAddress(marker.getLatLng().lat + " " + marker.getLatLng().lng)
                }
              },
            }),
            [],
          )
        return (
        <Marker
            draggable={true}
            eventHandlers={eventHandlers}
            position={home}
            icon={generic}
            ref={markerRef}>
            <Popup>
                <div className='popup'>
                    <h1>{showHome}</h1>
                    <div className='topPop'>
                        <div className='topleft inPop'>
                            <h2>Safety Score</h2>
                            <h4>{scores.safetyScore > 0 ? scores.safetyScore: null}</h4>
                        </div>

                        <div className='topright inPop'>
                            <h2>Park Score</h2>
                            <h4>{scores.parkScore > 0 ? scores.parkScore: null}</h4>
                        </div>
                    </div>
                    <div className='bottom inPop'>
                        <h2>Transportation Score</h2>
                        <h4>{scores.transportationScore > 0 ? scores.transportationScore: null}</h4>

                    </div>

                </div>
            </Popup>
        </Marker>
        )
    }

    function BikeData(){
        const bikeData = allMapData.bikeData
        if(bikeData.length > 0){
            let toShow = bikeData.map((each, index) =>{
                return(
                    <Polyline key={index} positions={each.coord}>
                    </Polyline>
                )
            })
            return toShow
        }
    }
    
    function TTCData(){
        const ttcData = allMapData.ttcData
        if(ttcData.ttcStations.length > 0){
            let toShow = ttcData.ttcStations.map((each, index)=>{
                if(each.address != ttcData.closestTTCStation.address){
                    return(
                        <Marker key={index} position={[each.coord[0], each.coord[1]]} icon={ttcIcon}>
                            <Popup>
                                {"TTC Station:"} <br />
                                {"Name: " + each.name} <br/>
                                {"Address: " + each.address} <br/>
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br />
                            </Popup>
                        </Marker>
                    )
                }
                else{
                    return(
                        <Marker icon={ttcIconMain} key={index} position={[each.coord[0], each.coord[1]]}>
                            <Popup>
                                {"TTC Station:"} <br />
                                {"Name: " + each.name} <br/>
                                {"Address: " + each.address} <br/>
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br/>
                                {"CLOSEST TTC STATION"}
                            </Popup>
                        </Marker>
                    )
                }
            })
            return toShow
        }
    }

    function HospitalData(){
        const hospitalData = allMapData.hospitalData

        if(hospitalData.allHospitalData.length > 0){
            let toShow = hospitalData.allHospitalData.map((each, index)=>{
                if(each.address != hospitalData.closestHospital.address){
                    return(
                        <Marker key={index} position={[each.coord[0], each.coord[1]]} icon={Hospitals}>
                            <Popup>
                                {"Name: " + each.name} <br/>
                                {"Address: " + each.address} <br/>
                                {"Distance: " + each.distance.toFixed(2)} <br />
                            </Popup>
                        </Marker>
                    )
                }
                else{
                    return(
                        <Marker key={index} position={[each.coord[0], each.coord[1]]} icon={Hospitalclose}>
                            <Popup>
                                {"Name: " + each.name} <br/>
                                {"Address: " + each.address} <br/>
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br/>
                                {"CLOSEST HOSPITAL"}
                            </Popup>
                        </Marker>
                    )
                }
            })
            return toShow
        }
    }

    function CrimeData() {
        const crimeData = allMapData.crimeData
        if (!crimeData){
            return
        }
        if(Object.keys(crimeData).length > 0){
            return(
                <Polygon positions={crimeData.poly} pathOptions={crimeDesign}>
                    <Popup>
                        {"Neighboorhood: " + crimeData.areaName} <br />
                        {"Population: " + crimeData.population} <br />
                        {"Id: " + crimeData.id} <br />
                        {"Crime: " + crimeData.crimeScore.toFixed(2)}
                    </Popup>
                </Polygon>
            )
        }
    }

    function FireData() {
        const fireStations = allMapData.fireData
        if (fireStations.allFireStations.length > 0) {
            let toshow = fireStations.allFireStations.map((each, index) => {
                if(each.address != fireStations.closestStation.address){
                    return(
                        <Marker key={index} position={[each.station[0], each.station[1]]} icon={fireTruck}>
                            <Popup>
                                {"Fire station:"} <br />
                                {"Address: " + each.address}<br />
                                {"Distance: " + each.distance.toFixed(2) + "km"}
                            </Popup>
                        </Marker>
                    )
                }
                else{
                    return(
                        <Marker key={index} position={[each.station[0], each.station[1]]} icon={fireTruckBig}>
                            <Popup>
                                {"Fire Station:"} <br />
                                {"Address: " + each.address}<br />
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br />
                                {"CLOSEST FIRE STATION"}
                            </Popup>
                        </Marker>
                    )
                }
            }
            );
            return toshow;
        }
    }

    function ParkDataFunction(){
        const parkData = allMapData.parkData
        if(parkData.allPark.length > 0){
            let toShow = parkData.allPark.map((each)=>{
                if(each.name != parkData.closestPark.name)
                    return (
                        <Polygon key={each.id} positions={each.poly} pathOptions={parkDesign}>
                            <Popup>
                                {"Name: " + each.name}<br />
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br />
                                {"Area: " + each.area.toFixed(2) + "m"}<br />
                                {"Id: " + each.id}
                            </Popup>
                        </Polygon>
                    )
                else{
                    return(
                        <Polygon key={each.id} positions={each.poly} pathOptions={parkDesignClose}>
                            <Popup>
                                {"Name: " + each.name}<br />
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br />
                                {"Area: " + each.area.toFixed(2) + "m"}<br />
                                {"Id: " + each.id} <br />
                                {"CLOSEST GREENSPACE"}
                            </Popup>
                        </Polygon>
                    )
                }
            })
            return toShow
        }
    }

    function handleKeyDown(event){
        if(event.key == "Enter"){
            changeAddress()
        }
    }

    function PoliceData() {
        const policeStations = allMapData.policeData
        if (policeStations.allDepartments.length > 0) {
            let toshow = policeStations.allDepartments.map((each, index) => {
                if(each.address != policeStations.closestDepartment.address){
                    return(
                    <Marker key={index} position={[each.location[1], each.location[0]]} icon={PoliceCar}>
                        <Popup>
                            {"ID: " + each.id}<br />
                            {"Address: " + each.address}<br />
                            {"Facility: " + each.facility}<br />
                            {"Distance: " + each.distance.toFixed(2) + "km"}
                        </Popup>
                    </Marker>
                    )
                }
                else{
                    return(
                        <Marker key={index} position={[each.location[1], each.location[0]]} icon={PoliceCarClose}>
                            <Popup>
                                {"ID: " + each.id}<br />
                                {"Address: " + each.address}<br />
                                {"Facility: " + each.facility}<br />
                                {"Distance: " + each.distance.toFixed(2) + "km"} <br />
                                {"CLOSEST POLICE STATION"}
                            </Popup>
                        </Marker>
                    )
                }

            });
            return toshow;
        }
    }

    function IconData(){
        return(
            <>
                {checked.police && <PoliceData />}
                {checked.fire && <FireData />}
                {checked.neighboorhood && <CrimeData/>}
                {checked.park && <ParkDataFunction/>}
                {checked.hospital && <HospitalData />}
                {checked.ttc && <TTCData />}
                {checked.bike && <BikeData />}
            </>
        )
    }
    

    return(
        <div className='mapComponent'>
            {loading == true? <div className='fullscreen'><img className='loadingIMG' src={loadingIMG} alt="LOADING..." /></div>: (
            <MapContainer className='actualMap' zoom={14} center={[home[0], home[1]]} scrollWheelZoom={false}>
                <TileLayer 
                    attribution='&copy; <a href="https://www.carto.com/attributions">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"/>
    
                <Circle center={[home[0], home[1]]} radius={5000} color='red' fillColor='transparent'>
                    <Popup>
                        {"Quick Drives: 5km"}
                    </Popup>
                </Circle>

                <Circle center={[home[0], home[1]]} radius={1500} pathOptions={circleDesign}>
                    <Popup>
                        {"Walking Distance Radius: 1.5km"}
                    </Popup>
                </Circle>

                <DraggableMarker />
                {loading == false ? <IconData /> : null}
    
            </MapContainer>
    )}
        <button onClick={onClickDrop} className='dropdown' style={{color: color}}>☰</button>
        <div className='legend' style={{width: legendStyle.width, paddingLeft: legendStyle.paddingleft, paddingRight: legendStyle.paddingright}}>
            <div className='formleg'>
                <a className="homeLink"  href="/">HOME</a>
                <label>
                    <input type="checkbox" id="fire" onChange={handleCheck} checked= {checked.fire}/>Fire
                    <img src="https://www.svgheart.com/wp-content/uploads/2021/11/fire-truck-emergency-vehicle-firefighter-free-svg-file-SvgHeart.Com-2.png" alt="firetruck" />
                </label>
                
                <label>
                    <input type="checkbox" id="hospital" onChange={handleCheck} checked= {checked.hospital} />Hospitals
                    <img src="https://static.vecteezy.com/system/resources/thumbnails/017/177/954/small/round-medical-cross-symbol-on-transparent-background-free-png.png" alt="hospital" />

                </label>

                <label>
                    <input type="checkbox" id="police" onChange={handleCheck} checked= {checked.police}/>Police
                    <img src="https://png.pngtree.com/png-vector/20230209/ourmid/pngtree-police-car-cartoon-png-image_6592485.png" alt="police" />
                </label>

                <label>
                    <input type="checkbox" id="ttc" onChange={handleCheck} checked= {checked.ttc}/>TTC
                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/Logo_of_the_Toronto_Transit_Commission.svg" alt="TTC" />
                </label>

                <label>
                    <input type="checkbox" id="bike" onChange={handleCheck} checked= {checked.bike}/>Bike
                    <img src={img} alt="Bike" />

                </label>

                <label>
                    <input type="checkbox" id="park" onChange={handleCheck} checked= {checked.park}/>Park
                    <img src={green} alt="Park" />

                </label>

                <label>
                    <input type="checkbox" id="neighboorhood" onChange={handleCheck} checked= {checked.neighboorhood}/>Neighboorhood
                    <img src={hood} alt="neighboorhood" />

                </label>
                <div className='inyo'>
                    <input onKeyDown={handleKeyDown} type="text" name="newAddress" id="newAddress" placeholder='Address' onChange={inputAddress}/>
                    <button className='button-86' onClick={changeAddress}>Change</button>
                </div>
                
            </div>

        </div>
        </div>
    )
    
    
}

