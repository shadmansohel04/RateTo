import { useEffect, useState } from "react";
import Header from "../components/headerComponent";
import SubmitAddressComponent from "../components/submitAddressBox";
import "../styles/submitAddressBox.css";
import { useNavigate } from "react-router-dom";

export default function FrontPage() {
    const nav = useNavigate();
    const [opacity, setOpacity] = useState("0%");
    const [padding, setPadding] = useState("100vh");

    useEffect(() => {
        const timer = setTimeout(() => {
            setOpacity("1");
            setPadding("0");
        }, 10);

    }, []);


    return (
        <div className="wholePage" style={{ opacity: opacity, paddingBottom: padding }} id="topofpage">
            <Header />
            <SubmitAddressComponent />
        </div>
    );
}
