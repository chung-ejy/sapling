import React, { useContext } from 'react';
import DataContext from '../../context/data/dataContext';

const KPITable = () => {
    const dataContext = useContext(DataContext);
    const { results, loading } = dataContext;

    return (
        
        <div className="container">
        <h3>Key Performance Indicators</h3>
        <div className="card card-body">
            <table>
                {Object.keys(results.kpi).length > 0 && !loading ? (
                         <tbody>
                        {Object.keys(results.kpi).map((key) => (
                            <tr key={key}>
                                <td>{key}</td><td>{results.kpi[key]}</td>
                            </tr>
                        ))}
                        </tbody>
                    ) : (
                        <tbody>
                        <tr>
                            <td colSpan="3">{loading ? 'Loading...' : 'No kpi available'}</td>
                        </tr>
                        </tbody>
                    )}
            </table>
        </div>
        </div>
    );
};

export default KPITable;
