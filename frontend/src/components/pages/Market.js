import React , { useContext, useEffect ,useState } from 'react';
import DataContext from '../../context/data/dataContext'

const Market = () => {
    const dataContext = useContext(DataContext)
    const { loading, market, getMarket, title } = dataContext
    const [state,setState] = useState(0)
    const onRange = (e) => {
        setState(Number(e.target.value));
    };

    useEffect(() => {
        getMarket()
    },[title])

  return (
    <div className="container">
      <h3>Market</h3>
      {loading || market.length < 1 ? "" :
      <div className="row">
         {market.slice(state,state+3).map((product, index) => (
          <div class="card">
            <div class="card-body">
              <table class="table table-striped">
                <tbody>
                  <tr>
                    <td><strong>Strategy</strong></td>
                    <td>{product.strategy}</td>
                  </tr>
                  <tr>
                    <td><strong>Standard Deviation</strong></td>
                    <td>{product.std}</td>
                  </tr>
                  <tr>
                    <td><strong>Coefficient of Variance</strong></td>
                    <td>{product.coefficient_of_variance}</td>
                  </tr>
                  <tr>
                    <td><strong>Sharpe Ratio</strong></td>
                    <td>{product.sharpe}</td>
                  </tr>
                  <tr>
                    <td><strong>Return</strong></td>
                    <td>{product.return}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        ))}
        <input type="range" className="form-control form-group form-range" onChange={onRange} min={0} max={Number(market.length - 1)} step={1} />
      </div>}
    
    </div>
  );
};

export default Market;
