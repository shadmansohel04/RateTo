import { useState } from "react";
import "../styles/contactBody.css";
import axios from "axios";

export default function ContactForm() {
    const [error, setError] = useState({
        msg: "",
        display: false
    });
    const [email, setEmail] = useState("");
    const [subject, setSubject] = useState("");
    const [message, setMessage] = useState("");

    function sendEmail() {
        axios.post("https://rateto-backend.onrender.com/contact", {
            info: {
                email,
                subject,
                message
            }
        })
        .then((response) => {
            if (response.data.success === true) {
                alert("Sent")
                setError({
                    msg: "",
                    display: false
                })
            } else {
                setError({
                    msg: response.data.msg || "Failed to send email",
                    display: true
                });
            }
        })
        .catch((error) => {
            console.error(error);
            setError({
                msg: "An error occurred. Please try again later.",
                display: true
            });
        });
    }

    return (
        <div className="contactForm">
            <h1>Contact Us</h1>
            <div className="form">
                {error.display && <p className="errorMSG">{error.msg}</p>}
                <h2>Email</h2>
                <input 
                    value={email} 
                    type="email" 
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Enter Email" 
                />
                <h2>Subject</h2>
                <input 
                    value={subject} 
                    type="text" 
                    onChange={(e) => setSubject(e.target.value)} 
                    placeholder="Enter Subject" 
                />
                <h2>Message</h2>
                <textarea 
                    value={message} 
                    onChange={(e) => setMessage(e.target.value)} 
                    id="message" 
                    rows="5" 
                    placeholder="Message"
                ></textarea>
                <button className="button-28" onClick={sendEmail}>Send</button>
            </div>
        </div>
    );
}
