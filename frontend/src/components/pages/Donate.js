import React from 'react';
import venmo from '../../assets/venmo_QR.png';
import paypal from '../../assets/paypal_QR.JPG';

const Donate = () => {
  return (
    <div className="container mt-5 text-center">
      <h1 className="text-primary">Donate to upgrade our server!</h1>
      <div className="row">
        <div className="col-md-6">
          <img
            src={venmo}
            style={{
              objectFit: 'cover',
              height: '50%',
            }}
            className="img-fluid p-3" // Adjust padding as needed
            alt="Venmo QR Code"
          />
        </div>
        <div className="col-md-6">
          <img
            src={paypal}
            style={{
              objectFit: 'cover',
              height: '50%',
            }}
            className="img-fluid p-3" // Adjust padding as needed
            alt="PayPal QR Code"
          />
        </div>
      </div>
    </div>
  );
};

export default Donate;
