import React from 'react';
import LandingCard from '../cards/LandingCard';
import LearnCard from '../cards/LearnCard';
import dashboard from '../../assets/dashboard.png';

const Landing = () => {
  return (
    <div className="container mt-10 text-center">
      <h1 className="text-primary">Algorithmic Stock Trading Platform</h1>
      <img
        src={dashboard} // Replace with the actual path to your image
        className="img-fluid p-5 size-50" // Use img-fluid for responsive images
        alt="Card Image"
      />
      <h3 className="text-primary"></h3>
      <div className="row align-item-center text-center">
        <div className="col-md-5">
          <LandingCard />
        </div>
        <div className="col-md-5">
          <LearnCard />
        </div>
      </div>
    </div>
  );
};

export default Landing;
