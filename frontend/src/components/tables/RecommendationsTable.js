import React, { useContext, useState } from 'react';
import DataContext from '../../context/data/dataContext';

const RecommendationsTable = () => {
    const [state, setState] = useState(0);
    const dataContext = useContext(DataContext);
    const { results, loading } = dataContext;

    const onRange = (e) => {
        setState(Number(e.target.value));
    };

    const downloadCSV = () => {
        const csvData = convertToCSV(results.recommendations);
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'recommendations.csv';
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
        <h3>Recommendations</h3>
        <div className="card card-body">
            <table>
                <thead>
                    <tr>
                        <th>date</th>
                        <th>ticker</th>
                        <th>signal</th>
                    </tr>
                </thead>
                <tbody>
                    {results.recommendations.length > 0 && !loading ? (
                        results.recommendations.slice(state, state + 5).map((trade, index) => (
                            <tr key={index}>
                                <td>{trade.date}</td>
                                <td>{trade.ticker}</td>
                                <td>{trade.signal}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="3">{loading ? 'Loading...' : 'No recommendations available'}</td>
                        </tr>
                    )}
            </tbody>
            </table>
            <input type="range" className="form-control form-group form-range"onChange={onRange} min={0} max={Number(results.recommendations.length - 1)} step={1} />
            <button onClick={downloadCSV}>Download</button>
        </div>
        </div>
    );
};

export default RecommendationsTable;
