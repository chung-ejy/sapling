import React, { useContext, useEffect, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const ParameterForm = () => {
  const dataContext = useContext(DataContext);
  const { tickers, strategies, title, getStrategy, getTickers, backtest } = dataContext;

  const [state, setState] = useState({
    strategy: 'COEFFICIENT_OF_VARIANCE',
    ascending: 'False',
    holding_period: 5,
    positions: 1,
    stop_loss: 0.05,
    tickers: []
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

  // const onSelect = (e) => {
  //   e.preventDefault();
  //   setState({
  //     ...state,
  //     [e.target.name]: [...state[e.target.name], e.target.value],
  //   });
  // };

  const onAdd = (e) => {
    e.preventDefault();
    setState({
      ...state,
      [e.target.name]: [...state[e.target.name], e.target.value],
    });
  };

  const onDelete = (e, ticker) => {
    e.preventDefault();
    setState({
      ...state,
      tickers: state.tickers.filter((item) => item !== ticker),
    });
  };

  const onSubmit = (e) => {
    e.preventDefault();
    backtest(state);
  };

  return (
    <div className="container mt-4">
      <h3 className="text-center mb-4">Parameter Form</h3>
      <div className="row">
        <div className="col-md-6">
          <div className="card shadow">
            <div className="card-body">
              <form onSubmit={onSubmit}>
                <div className="mb-3">
                  <label htmlFor="strategy" className="form-label">
                    Strategy
                  </label>
                  <select
                    onChange={onChange}
                    name="strategy"
                    className="form-select"
                    value={state.strategy}
                  >
                    {strategies.map((strategy, index) => (
                      <option key={index}>{strategy}</option>
                    ))}
                  </select>
                </div>

                <div className="mb-3">
                  <label htmlFor="tickers" className="form-label">
                    Tickers
                  </label>
                  <select
                    onChange={onAdd}
                    name="tickers"
                    className="form-select"
                    value={state.ticker}
                  >
                    {tickers.map((ticker, index) => (
                      <option key={index}>{ticker}</option>
                    ))}
                  </select>
                  {/* <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => onAdd(e)}
                >
                  <span aria-hidden="true">&times;</span>
                </button> */}
                </div>

                <div className="mb-3">
                  <label htmlFor="ascending" className="form-label">
                    Ascending
                  </label>
                  <select
                    onChange={onChange}
                    name="ascending"
                    className="form-select"
                    value={state.ascending}
                  >
                    <option>true</option>
                    <option>false</option>
                  </select>
                </div>

                <div className="mb-3">
                  <label htmlFor="positions" className="form-label">
                    Positions: {state.positions}
                  </label>
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

                <div className="mb-3">
                  <label htmlFor="stop_loss" className="form-label">
                    Stop Loss: {state.stop_loss}
                  </label>
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

                <button type="submit" className="btn btn-primary w-100">
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <ul className="list-group">
            {state.tickers.map((ticker) => (
              <li
                key={ticker}
                className="list-group-item d-flex justify-content-between align-items-center"
              >
                {ticker}
                <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => onDelete(e, ticker)}
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ParameterForm;
