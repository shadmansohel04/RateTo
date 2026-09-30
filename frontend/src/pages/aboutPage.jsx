import Header from "../components/headerComponent"
import AboutBody from "../components/aboutBody";
import { useEffect, useState } from "react";
import "../styles/transition.css"

export default function AboutPage(){
    const [padding, setPadding] = useState("40vh")
    const [opacity, setOpacity] = useState("0")

    useEffect(()=>{
        const timer = setTimeout(()=>{
            setPadding("0")
            setOpacity("100")
        }, 10)
    }, [])

    return(
        <div className="pageTransition" style={{opacity: opacity, paddingBottom: padding}}>
            <Header />
            <AboutBody />
        </div>
    )
}