import React from 'react';

const OverviewCard = () => {
    return (
        <div className="card shadow">
            <div className="card-body">
                <h3 className="card-title">Overview</h3>
                <p className="card-text">
                    The algorithm for this specific backtest ranks stocks by a specific signal chosen by the user.
                    The algorithm then ranks by ascending or descending order and chooses the top stocks in said order.
                    The algorithm then buys the stock at market price (market order).
                    The algorithm sets a stop-loss order set by a percentage of the previous day's price.
                    The algorithm then holds the stock for exactly one week and sells the stock at the end of one week (5 business days).
                    The algorithm does not short stocks.
                    Recommendations are updated 2 hours before the market opens.
                </p>
            </div>
        </div>
    );
};

export default OverviewCard;
