import React from 'react';
import DataState from './context/data/dataState';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './components/pages/Landing';
import Dashboard from './components/pages/Dashboard';
import Learn from './components/pages/Learn';
import Donate from './components/pages/Donate';

const App = () => {
    return (
        <DataState>
            <Router>
                <Header />
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/learn" element={<Learn />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    {/* <Route path="/donate" element={<Donate />} /> */}
                </Routes>
                <Footer />
            </Router>
        </DataState>
    );
};

export default App;
