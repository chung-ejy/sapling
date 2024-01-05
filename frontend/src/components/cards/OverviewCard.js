
import React from 'react';

const OverviewCard = () => {
  return (
    <div className="card shadow">
      <div className="card-body">
        <h1 className="card-title mb-4">Overview</h1>

        <div className="client-info">
          <h5 className="section-title">Description of Client</h5>
          <p>An individual seeking a consistent quantitative stock allocation strategy across a short term time horizon.</p>
        </div>

        <div className="purpose-section">
          <h5 className="section-title">Statement of Purpose</h5>
          <p>
            The purpose of this application and framework is to provide educational, research, and deployment resources for weekly quantitative stock picking strategies.
          </p>
        </div>

        <div className="procedures-section">
          <h5 className="section-title">Procedures</h5>
          <p>            
            The day starts by retrieving updated stock price data during pre-market hours.
            The user will then fill out the dashboard form to communicate the signal to be researched and backtested.
            The code algorithm will then calculate the signal for each stock, rank them accordingly and choose the appropriate assets to recommend.
            From this point, the backtest portion of the application begins.
            The backtest is based on historical stock price data and is a simulation of the orders the algorithm would make given historical
            market conditions.
            The backtest reads the historical recommendations, places a market order for the chosen tickers, sets a stop-order, and closes all positions
            after a five day holding period.
            The backtest does not short stocks and instead only places market buy orders to open a position.
            At the end of the backtest, the application will provide you with historical trades, the most up to date stock recommendations, and key Performance
            indicators.
          </p>
        </div>

        <div className="objective-section">
          <h5 className="section-title">Application Objective</h5>
          <p>
            The goal of this application is to provide multiple quick, easy, and accessible methods of screening stocks and communicate the value add of consistent investment practices.
          </p>
        </div>

        <div className="constraints-section">
          <h5 className="section-title">Application Constraints</h5>
          <p>
            The application tracks up to seven given tickers provided by the user. Tickers must be included in the S&P100. The application backtests for a maximum of 2 years. Strategies are technically driven and are not based on financial statement stock data.
          </p>
        </div>

        <div className="guidelines-section">
          <h5 className="section-title">Application Guidelines</h5>
          Despite the comprehensive strategies given and the consistency of the provided algorithm, historical returns and results are not 
          an indicator of future returns or performance. The resources provided in this app are for educational purposes and in no way reflect
          professional financial advice. Please seek a professional and licensed financial advisor before making any investment decisions.  
        </div>

      </div>
    </div>
  );
};

export default OverviewCard;