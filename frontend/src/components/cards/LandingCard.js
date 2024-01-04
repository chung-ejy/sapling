import React from 'react'
import { Link } from 'react-router-dom';

const LandingCard = () => {
    return (
            <div className="card">
            <div className="card-body">
                <h3 className="card-text">Research and backtest different weekly trading algorithms for the S&P100.</h3>
                <h5>Receive historical trades and current recommendations!</h5>
                <Link  to="/dashboard"><button className="btn btn-primary text-light">Try it out!</button></Link>
            </div>
            </div>
    )
}

export default LandingCard