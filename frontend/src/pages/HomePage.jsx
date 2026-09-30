import { useEffect, useState } from "react"
import MapComponent from "../components/map"
import { useParams } from "react-router-dom"

export default function HomePage(){
    const [address, setAddress] = useState("")
    const params = useParams()
    useEffect(()=>{
        let newAddress = params.address.replace(/\+/g, " ")
        setAddress(newAddress)
    }, [])


    if (address != ""){
        return(
            <>
                <MapComponent address={address}/>
            </>
        )
    }
}