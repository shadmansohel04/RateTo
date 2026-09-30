import Header from "../components/headerComponent"
import ContactForm from "../components/contactForm"
import { useState, useEffect } from "react"
import "../styles/transition.css"

export default function ContactPage(){
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
            <ContactForm />
        </div>
    )
}