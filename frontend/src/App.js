import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Outlet } from 'react-router-dom';
import DataState from './context/data/dataState';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Landing from './components/pages/Landing';
import Research from './components/pages/Research';
import Learn from './components/pages/Learn';
import Login from './components/pages/Login';

const isAuthenticated = () => {
    const token = localStorage.getItem("token");
    return token !== null; // Replace with your authentication logic
};

const PrivateRoute = () => {
    const auth = isAuthenticated(); // determine if authorized, from context or however you're doing i
    return auth ? <Outlet /> : <Navigate to="/login" />;
}

const App = () => {
    return (
        <DataState>
            <Router>
                <Header />
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/research" element={<Research />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/learn" element={<Learn />} />
                </Routes>
                <Footer />
            </Router>
        </DataState>
    );
};

export default App;
