import React, { Fragment , useContext } from 'react';
import DataState from './context/data/dataState';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './components/pages/Landing';
import Dashboard from './components/pages/Dashboard';
import Learn from './components/pages/Learn';
import Donate from './components/pages/Donate';
import Authentication from './components/pages/Authentication';
import DataContext from './context/data/dataContext';
const App = () => {
    const dataContext = useContext(DataContext)
    const { isAuth, authToken } = dataContext
    return (
        <DataState>
            <Router>
                <Header />
                <Routes>
                    {isAuth ? <Route path="/" element={<Landing />} /> : <Route path="/dashboard" element={<Dashboard />} />}
                    {isAuth ? <Route path="/authentication" element={<Authentication />} /> : ""}
                    <Route path="/learn" element={<Learn />} />
                </Routes>
                <Footer />
            </Router>
        </DataState>
    );
};

export default App;
