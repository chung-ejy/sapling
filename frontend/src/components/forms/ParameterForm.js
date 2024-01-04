import React, { useContext, useEffect, useState } from 'react'
import DataContext from '../../context/data/dataContext'
const ParameterForm = () => {
    const dataContext = useContext(DataContext)
    const { strategies , title , getStrategy, backtest} = dataContext
    const [state,setState] = useState({"strategy":"COEFFICIENT_OF_VARIANCE"
                                        ,"ascending":"False"
                                        ,"holding_period":5
                                        ,"positions":10
                                        ,"stop_loss":0.05
                                    })
    useEffect(() => {
        getStrategy()
    // eslint-disable-next-line
    },[title]
    )
    const onChange = (e) => {
        e.preventDefault()
        setState({
            ...state,[e.target.name]: e.target.value
        })
    }

    const onSubmit = (e) => {
        e.preventDefault()
        backtest(state)
    }
    
    return (
        <div className="container m-5">
        <h3>Parameter Form</h3>
        <div className="card card-body">
        <form className="form" onSubmit={onSubmit}>
            <table>
            <tbody>
                <tr className="form-group">
                    <td>{`strategy`}</td>
                    <td>{state.strategy}</td>
                    <td><select onChange={onChange} name="strategy" className="form-select form-select-sm" 
                        defaultValue={state.strategy} aria-label="Small select example">
                        {strategies.map((strategy,index) => (<option key={index}>{strategy}</option>))}
                    </select></td>
                </tr>
        
        <tr className="form-group">
        <td>{`ascending`}</td>
        <td>{state.ascending}</td>
        <td><select onChange={onChange} name="ascending" className="form-select form-select-sm" 
            defaultValue={state.ascending} aria-label="Small select example">
            <option key={true}>{"True"}</option>
            <option key={false}>{"False"}</option>
        </select></td>
        </tr>
        

        <tr className="form-group">
        <td>{`holding_period`}</td>
        <td>{state.holding_period}</td>
        <td><input type="range" onChange={onChange} name="holding_period" 
                        className="form-range col" min="5" max="65" step="5" 
                        placholder="" id="customRange2" /></td>
        </tr>

        <tr className="form-group">
        <td>{`positions`}</td>
        <td>{state.positions}</td>
        <td><input type="range" onChange={onChange} name="positions" 
                        className="form-range col" min="5" max="25" step="5" 
                        placholder="" id="customRange2" /></td>
        </tr>

        <tr className="form-group">
        <td>{`stop_loss`}</td>
        <td>{state.stop_loss}</td>
        <td><input type="range" onChange={onChange} name="stop_loss" 
                        className="form-range col" min="0" max="0.5" step=".05" 
                        placholder="" id="customRange2" /></td>
        </tr>
        </tbody>
        </table>
        <button type="submit" className="btn btn-primary btn-block align-center">Submit</button>
        </form>
        </div>
        </div>

    )
}

export default ParameterForm