import React, { useContext, useState, useEffect } from 'react';
import DataContext from '../../context/data/dataContext';
import StrategyDescriptionCard from '../cards/StrategyDescriptionCard';
import OverviewCard from '../cards/OverviewCard';
import ParameterCard from '../cards/ParameterCard';

const Learn = () => {
    const dataContext = useContext(DataContext);
    const { title, getStrategy, getDescription ,strategies, descriptions, loading } = dataContext;
    const [state, setState] = useState({"strategy":"overview","dropdown":false});
    
    useEffect(()=>{
        getStrategy()
        getDescription()
        // eslint-disable-next-line
    },[title])

    const setSelectedStrategy = (strat) => {
        setState({
            ...state,
            ["strategy"]:strat
        })
    }
    const toggleDropdown = (e) => {
        e.preventDefault()
        setState({
            ...state,
            ["dropdown"]:!state.dropdown
        })
    }
    return (
        <div className="row mt-3">
            <div className="col-md-2">
                <ul className="list-group">
                    <li className="list-group-item" onClick={() => setSelectedStrategy("overview")}>overview</li>
                    <li className="list-group-item" onClick={() => setSelectedStrategy("parameter")}>parameter</li>
                    <li className="list-group-item" onClick={toggleDropdown}>strategies</li>
                    {strategies.length < 1 || state.dropdown === false || loading
                        ? ''
                        : strategies.map((strategy, index) => (
                              <li className="list-group-item" key={index} onClick={() => setSelectedStrategy(strategy)}>
                                  {strategy.toLowerCase().replace('_', ' ')}
                              </li>
                          ))}
                </ul>
            </div>
            <div className="col-md-7">
                {(() => {
                    switch (state.strategy) {
                        case 'overview':
                            return <OverviewCard />
                        case 'parameter':
                            return <ParameterCard />
                        default:
                            return <StrategyDescriptionCard description={descriptions[state.strategy]}/>;;
                    }
                })()}
            </div>
        </div>
    );
};

export default Learn;
