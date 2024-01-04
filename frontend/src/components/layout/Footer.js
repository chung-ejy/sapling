import React from 'react';
import { Link } from 'react-router-dom';
const Footer = () => {
    return (
        <footer className="footer mt-5 text-left text-light bg-primary" style={footerStyle}>
            <div className="container">
                <div className="row">
                    <div className="col-md-6">
                        <p>&copy; 2023 Eric Chung</p>
                        <p>Contact: chung.ejy@gmail.com</p>
                        {/* <p>
                            <Link to="/donate" className="navbar-brand">
                                <img alt=""/>
                                {"Donate"}
                            </Link>
                        </p> */}
                        <p>Disclaimer: Consult an investment advisor before making any investment decisions.</p>
                    </div>
                    <div className="col-md-6">
                        <p>
                            Icons by{' '}
                            <a href="https://www.flaticon.com/free-icons/christmas" title="christmas icons">
                                Pixel perfect - Flaticon
                            </a>
                        </p>
                        <p>
                            Powered by{' '}
                            <a href="https://alpaca.markets/" target="_blank" rel="noopener noreferrer">
                                Alpaca
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
};

const footerStyle = {
    textAlign: 'center',
    backgroundColor: '#f8f9fa', // Change the background color as needed
    padding: '20px',
    position: 'relative',
    bottom: 0,
    width: '100%',
};

export default Footer;
