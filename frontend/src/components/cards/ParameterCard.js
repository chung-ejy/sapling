import React from 'react';

const ParameterCard = () => {
    return (
        <div className="card shadow">
            <div className="card-body">
                <h3 className="card-title">Parameter</h3>
                <p className="card-text">
                    Parameters are created when you fill out the dashboard form.
                    The strategy dropdown defines which strategy you'll be using.
                    The ascending dropdown defines whether you'll be sorting signals in ascending or descending values.
                    The positions slider lets us know how many stocks you want in your portfolio.
                    The stop loss slider lets us know at what percentage loss you want to sell your position.
                </p>
            </div>
        </div>
    );
};

export default ParameterCard;
