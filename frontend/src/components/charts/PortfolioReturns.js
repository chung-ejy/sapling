import React, { useContext } from 'react';
import { VictoryChart, VictoryLine, VictoryAxis } from 'victory';
import DataContext from '../../context/data/dataContext';

const LineChart = () => {
  const dataContext = useContext(DataContext);
  const { results, loading } = dataContext;

  const formatDate = (dateString) => {
    const options = { month: 'numeric', day: 'numeric', year: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    loading || results.portfolio.length < 1 ? "" :
    <VictoryChart width={500} height={200}>
      <VictoryLine
        data={results.portfolio}
        x={(x) => new Date(x.date)}
        y="cumulative_return"
        style={{
          data: { stroke: '#3f51b5', strokeWidth: 2 },
        }}
      />
      <VictoryAxis dependentAxis style={{ tickLabels: { fontSize: 10, padding: 5 } }} />
      <VictoryAxis
        tickFormat={(date) => formatDate(date)}
        style={{
          tickLabels: { fontSize: 10, padding: 5 },
        }}
      />
    </VictoryChart>
  );
};

export default LineChart;
