import React, { useContext, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const TradesTable = () => {
    const [state, setState] = useState(0);
    const dataContext = useContext(DataContext);
    const { results, loading } = dataContext;

    // const onRange = (e) => {
    //     setState(Number(e.target.value));
    // };

    const downloadCSV = () => {
        const csvData = convertToCSV(results.trades);
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'trades.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    };

    const convertToCSV = (data) => {
        const headers = Object.keys(data[0]);
        const csv = [
            headers.join(','),
            ...data.map((row) => headers.map((header) => row[header]).join(',')),
        ];
        return csv.join('\n');
    };

    return (
        <div className="container">
        <h3>Trades</h3>
        <div className="card card-body">
        <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>date</th>
                        <th>ticker</th>
                        {/* <th>{String.lowercase(parameter.strategy)}</th> */}
                        <th>return</th>
                    </tr>
                </thead>
                <tbody>
                    {results.trades.length > 0 && !loading ? (
                        // .trades.slice(state, state + 5)
                        results.trades.map((trade, index) => (
                            <tr key={index}>
                                <td>{trade.date}</td>
                                <td>{trade.ticker}</td>
                                {/* <td>{trade[String.lowercase(parameter.strategy)]}</td> */}
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
            </div>
            {/* <input type="range" className="form-control form-group form-range"onChange={onRange} min={0} max={Number(results.trades.length - 1)} step={1} /> */}
            <button className="btn btn-primary w-100" onClick={downloadCSV}>Download</button>
        </div>
        </div>
    );
};

export default TradesTable;
