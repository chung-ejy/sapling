import React from 'react';
import ParameterFormV3 from '../forms/ParameterFormV3';
import TradesTable from '../tables/TradesTable';
import PortfolioReturns from '../charts/PortfolioReturns';
import RecommendationsTable from '../tables/RecommendationsTable';
import KPITable from '../tables/KPITable';

const Dashboard = () => {
  
  return (
    <div className="row text-center">
      <div className="col-md-6">
        <div className="row">
          <div className="col-md-12">
            <PortfolioReturns />
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            <TradesTable />
          </div>
          <div className="col-md-6">
            <RecommendationsTable />
          </div>
        </div>
      </div>
      <div className="col-md-4">
        <ParameterFormV3 />
        <KPITable />
      </div>
    </div>
  );
};

export default Dashboard;
