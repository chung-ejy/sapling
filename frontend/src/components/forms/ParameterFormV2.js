import React, { useContext, useEffect, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const ParameterForm = () => {
  const dataContext = useContext(DataContext);
  const { strategies, title, getStrategy, backtest } = dataContext;

  const [state, setState] = useState({
    strategy: 'COEFFICIENT_OF_VARIANCE',
    ascending: 'False',
    holding_period: 5,
    positions: 10,
    stop_loss: 0.05,
  });

  useEffect(() => {
    getStrategy();
    // eslint-disable-next-line
  }, [title]);

  const onChange = (e) => {
    e.preventDefault();
    setState({
      ...state,
      [e.target.name]: e.target.value,
    });
  };

  const onSubmit = (e) => {
    e.preventDefault();
    backtest(state);
  };

  return (
    <div className="container mb-2 mt-2">
      <div className="card card-body">
        <form className="form" onSubmit={onSubmit}>
          <div className="row">
            <div className="col-md-6">
              <div className="form-group">
                <label htmlFor="strategy">Strategy</label>
                <select
                  onChange={onChange}
                  name="strategy"
                  className="form-select form-select-sm"
                  value={state.strategy}
                  aria-label="Strategy selection"
                >
                  {strategies.map((strategy, index) => (
                    <option key={index}>{strategy}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="col-md-6">
              <div className="form-group">
                <label htmlFor="ascending">Ascending</label>
                <select
                  onChange={onChange}
                  name="ascending"
                  className="form-select form-select-sm"
                  value={state.ascending}
                  aria-label="Ascending selection"
                >
                  <option key={1}>true</option>
                  <option key={2}>false</option>
                </select>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-md-4">
              <div className="form-group">
                <label htmlFor="holding_period">Holding Period: {state.holding_period}</label>
                <input
                  type="range"
                  onChange={onChange}
                  name="holding_period"
                  className="form-range"
                  min="5"
                  max="65"
                  step="5"
                  value={state.holding_period}
                  id="customRangeHoldingPeriod"
                />
              </div>
            </div>
            <div className="col-md-4">
              <div className="form-group">
                <label htmlFor="positions">Positions: {state.positions}</label>
                <input
                  type="range"
                  onChange={onChange}
                  name="positions"
                  className="form-range"
                  min="5"
                  max="25"
                  step="5"
                  value={state.positions}
                  id="customRangePositions"
                />
              </div>
            </div>
            <div className="col-md-4">
              <div className="form-group">
                <label htmlFor="stop_loss">Stop Loss: {state.stop_loss}</label>
                <input
                  type="range"
                  onChange={onChange}
                  name="stop_loss"
                  className="form-range"
                  min="0.05"
                  max="0.5"
                  step="0.05"
                  value={state.stop_loss}
                  id="customRangeStopLoss"
                />
              </div>
            </div>
          </div>

          <button type="submit" className="form-control btn btn-primary btn-small align-center">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default ParameterForm;
