import React, { useContext, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const TickersTable = () => {
    const [state, setState] = useState(0);
    const dataContext = useContext(DataContext);
    const { results, loading } = dataContext;

    const onRange = (e) => {
        setState(Number(e.target.value));
    };

    return (
        <div className="container">
        <h3>Trades</h3>
        <div className="card card-body">
            <table>
                <thead>
                    <tr>
                        <th>date</th>
                        <th>ticker</th>
                        <th>signal</th>
                        <th>return</th>
                    </tr>
                </thead>
                <tbody>
                    {results.trades.length > 0 && !loading ? (
                        results.trades.slice(state, state + 5).map((trade, index) => (
                            <tr key={index}>
                                <td>{trade.date}</td>
                                <td>{trade.ticker}</td>
                                <td>{trade.signal}</td>
                                <td>{trade.return}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="3">{loading ? 'Loading...' : 'No trades available'}</td>
                        </tr>
                    )}
            </tbody>
            </table>
            <input type="range" className="form-control form-group form-range"onChange={onRange} min={0} max={Number(results.trades.length - 1)} step={1} />
            <button onClick={downloadCSV}>Download</button>
        </div>
        </div>
    );
};

export default TradesTable;
