import React, { Fragment , useContext } from 'react';
import DataState from './context/data/dataState';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './components/pages/Landing';
import Dashboard from './components/pages/Dashboard';
import Learn from './components/pages/Learn';
import Donate from './components/pages/Donate';
import Signup from './components/pages/Signup';
import Login from './components/pages/Login'
const App = () => {
    const token = localStorage.getItem("authToken")
    console.log(token)
    return (
        <DataState>
            <Router>
                <Header />
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/learn" element={<Learn />} />
                </Routes>
                <Footer />
            </Router>
        </DataState>
    );
};

export default App;
