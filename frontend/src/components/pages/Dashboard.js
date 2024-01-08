import React from 'react';
import ParameterForm from '../forms/ParameterForm';
import TradesTable from '../tables/TradesTable';
import PortfolioReturns from '../charts/PortfolioReturns';
import RecommendationsTable from '../tables/RecommendationsTable';
import KPITable from '../tables/KPITable';
import Market from './Market';

const Dashboard = () => {
  
  return (
    <div className="row text-center">
      <div className="col">
        <div className="row">
          <div className="col">
            <PortfolioReturns />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <TradesTable />
          </div>
          <div className="col">
            <RecommendationsTable />
          </div>
        </div>
      </div>
      <div className="col">
        <ParameterForm />
        <KPITable />
      </div>
      <div className="col">
        <Market />
      </div>
    </div>
  );
};

export default Dashboard;
