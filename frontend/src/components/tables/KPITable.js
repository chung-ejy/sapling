import React, { useContext } from 'react';
import DataContext from '../../context/data/dataContext';

const KPITable = () => {
  const dataContext = useContext(DataContext);
  const { results, loading } = dataContext;

  return (
    <div className="container">
      <h3 className="text-center mt-4 mb-3">Key Performance Indicators</h3>
      <div className="card shadow">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-bordered table-striped">
              {Object.keys(results.kpi).length > 0 && !loading ? (
                <tbody>
                  {Object.keys(results.kpi).map((key) => (
                    <tr key={key}>
                      <td>{key}</td>
                      <td>{results.kpi[key]}</td>
                    </tr>
                  ))}
                </tbody>
              ) : (
                <tbody>
                  <tr>
                    <td colSpan="2" className="text-center">
                      {loading ? 'Loading...' : 'No KPI available'}
                    </td>
                  </tr>
                </tbody>
              )}
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KPITable;
