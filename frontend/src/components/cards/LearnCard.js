import React from 'react'
import { Link } from 'react-router-dom';

const LandingCard = () => {
    return (
            <div className="card">
            <div className="card-body">
                <h3 className="card-text">Learn about weekly stock trading algorithms and mistletoe's custom algorithms</h3>
                <h5 className="card-text">See the underlying code behind each strategy</h5>
                <Link  to="/learn"><button className="btn btn-primary text-light">Learn!</button></Link>
            </div>
            </div>
    )
}

export default LandingCard