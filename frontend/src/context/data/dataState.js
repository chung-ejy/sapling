import { GET_TOKEN, GET_STRATEGY, BACKTEST, SET_LOADING, STOP_LOADING, SET_ERROR, CLEAR_ERROR, GET_DESCRIPTION } from "./types";
import React, { useReducer } from "react";
import DataContext from "./dataContext"
import dataReducer from "./dataReducer"
import axios from "axios"

const DataState = props => {
    
    const initialState = {
        title: "mistletoe",
        strategies:[],
        descriptions:[],
        results:{"portfolio":[],"trades":[],"recommendations":[],"kpi":{}},
        error:null,
        loading:false,
        genres:[]
    }

    // const base_url = "https://mistletoe-api.onrender.com"
    // const base_url = "http://localhost:8000"
    const base_url = ""
    const [state,dispatch] = useReducer(dataReducer,initialState)

    const setError = (msg,type) => {
        dispatch({
            type:SET_ERROR,
            payload: {msg,type}
        })
        setTimeout(()=> {
            clearError()
        },5000);
    }

    const clearError = () => {
        dispatch({
            type:CLEAR_ERROR
        });
    }

    const setLoading = () => {
        dispatch({
            type:SET_LOADING
        });
    }
    
    const stopLoading = () => {
        dispatch({
            type:STOP_LOADING
        });
    }

    const getStrategy = () => {
        setLoading()
        axios.get(`${base_url}/info/strategy`, {},).then(res=>{
            dispatch({
                type:GET_STRATEGY,
                payload:res.data
            })
        }).catch(err => {
            stopLoading()
            setError(err.message,"danger")
        });
    }

    const getToken = () => {
        setLoading()
        axios.get(`${base_url}/security_functions/token`, {}, {}).then(res=>{
            dispatch({
                type:GET_TOKEN,
                payload:res.data
            })
        }).catch(err => {
            stopLoading()
            setError(err.message,"danger")
        });
    }

    const getTokenV2 = async () => {
        setLoading()
        const res = await axios.get(`${base_url}/security_functions/token`, {}, {})
        stopLoading()
        return res.data.csrf_token
    }

    const getDescription = () => {
        setLoading()
        axios.get(`${base_url}/info/strategy/descriptions`, {}, ).then(res=>{
            dispatch({
                type:GET_DESCRIPTION,
                payload:res.data
            })
        }).catch(err => {
            stopLoading()
            setError(err.message,"danger")
        });
    }

    const backtestAwait = (data) => {
        getTokenV2().then(token =>{
            backtest(data,token)
        })
    }

    const backtest = (data,token) => {
        setLoading();
        axios.post(`${base_url}/backtest/`,data, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': token
            },
          }).then(res => {
            dispatch({
                type: BACKTEST,
                payload: res.data
            });
        }).catch(err => {
            stopLoading();
            setError(err.message, "danger");
        });
    };

    return (
        <DataContext.Provider value={{
            strategies:state.strategies,
            descriptions:state.descriptions,
            results:state.results,
            loading:state.loading,
            error:state.error,
            title:state.title,
            text:state.text,
            getStrategy,
            getDescription,
            backtest,
            backtestAwait
        }}>
            {props.children}
        </DataContext.Provider>
    )
}
export default DataState;