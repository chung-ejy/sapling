import React, { useContext, useEffect, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const ParameterForm = () => {
  const dataContext = useContext(DataContext);
  const { tickers, strategies, title, getStrategy, getTickers, backtestAwait } = dataContext;

  const [state, setState] = useState({
    strategy: 'COEFFICIENT_OF_VARIANCE',
    ascending: 'False',
    holding_period: 5,
    positions: 1,
    stop_loss: 0.05,
    tickers:[]
  });

  useEffect(() => {
    getStrategy();
    getTickers();
    // eslint-disable-next-line
  }, [title]);

  const onChange = (e) => {
    e.preventDefault();
    setState({
      ...state,
      [e.target.name]: e.target.value,
    });
  };

  const onSelect = (e) => {
    e.preventDefault();
    setState({
      ...state,
      [e.target.name]: [...state[e.target.name],e.target.value],
    });
  };

  const onDelete = (e,ticker) => {
    e.preventDefault()
    setState({
      ...state,
      ["tickers"]: [...state["tickers"].filter(item => item !== ticker).slice(0,7)],
    });
  };

  const onSubmit = (e) => {
    e.preventDefault();
    backtestAwait(state)
  };

  return (
    <div className="container">
      <h3>Form</h3>
      <div className="row">
      <div className="card card-body col-md-6">
        <form className="form" onSubmit={onSubmit}>
              <div className="form-group row">
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

              <div className="form-group row">
                <label htmlFor="tickers">Tickers</label>
                <select
                  onChange={onSelect}
                  name="tickers"
                  className="form-select form-select-sm"
                  value={state.tickers}
                  aria-label="tickers selection"
                  >
                  {tickers.map((ticker, index) => (
                    <option key={index}>{ticker}</option>
                  ))}
                </select>
              </div>

              <div className="form-group row">
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

              <div className="form-group row">
                <label htmlFor="positions">Positions: {state.positions}</label>
                <input
                  type="range"
                  onChange={onChange}
                  name="positions"
                  className="form-range"
                  min="1"
                  max="5"
                  step="1"
                  value={state.positions}
                  id="customRangePositions"
                />
              </div>

              <div className="form-group row">
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
          <button type="submit" className="form-control btn btn-primary btn-small align-center">
            Submit
          </button>
        </form>
        </div>
        <ul className="list-group col-md-4">
          {state.tickers.map((ticker) => (
            <li key={ticker} className="list-group-item d-flex justify-content-between align-items-center">
              {ticker}
              <button
                className="btn btn-danger btn-sm"
                onClick={(e) => onDelete(e, ticker)}>
                <span aria-hidden="true">&times;</span>
              </button>
            </li>
          ))}
        </ul>
        </div>
      </div>
  );
};

export default ParameterForm;
