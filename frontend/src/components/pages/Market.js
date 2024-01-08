import React , { useContext, useEffect } from 'react';
import DataContext from '../../context/data/dataContext'

const Market = () => {
    const dataContext = useContext(DataContext)
    const { loading, market, getMarket, title } = dataContext

    useEffect(() => {
        getMarket()
    },[title])
    console.log(market)
  return (
    <div className="container">
      <h3>Market</h3>
      <div className="row">
        {loading || market.length < 1? "" : market.map((product, index) => (
          <div className="card mb-4">
            <div className="card-body">
              <p className="card-title">{product.strategy}</p>
              <p className="card-text">{product.return}</p>
              <p className="card-text">{product.sharpe}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Market;
