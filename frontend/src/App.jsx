import React from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import FrontPage from './pages/frontPage';
import AboutPage from './pages/aboutPage';
import ContactPage from './pages/contactPage';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<FrontPage />} />
        <Route path='/map/:address' element={<HomePage />}/>
        <Route path='/about' element={<AboutPage />}/>
        <Route path='/contact' element= {<ContactPage />}/>
      </Routes>
    </BrowserRouter>

  )
}

export default App
