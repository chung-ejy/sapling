import { LOGIN, LOGOUT, SIGNUP, GET_TICKERS,  GET_STRATEGY, BACKTEST, SET_LOADING, STOP_LOADING, SET_ERROR, CLEAR_ERROR, GET_DESCRIPTION } from "./types";
import React, { useReducer } from "react";
import DataContext from "./dataContext"
import dataReducer from "./dataReducer"
import axios from "axios"

const DataState = props => {
    
    const initialState = {
        title: "mistletoe",
        isAuth:false,
        authToken:"",
        user:null,
        tickers:[],
        strategies:[],
        descriptions:[],
        results:{"portfolio":[],"trades":[],"recommendations":[],"kpi":{}},
        error:null,
        loading:false,
        genres:[]
    }

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

    const getToken = async () => {
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

    const getTickers = () => {
        setLoading()
        axios.get(`${base_url}/info/tickers`, {}, ).then(res=>{
            dispatch({
                type:GET_TICKERS,
                payload:res.data
            })
        }).catch(err => {
            stopLoading()
            setError(err.message,"danger")
        });
    }

    const backtest = (data) => {
        setLoading();
        getToken().then(token => axios.post(`${base_url}/backtest/`,data, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': token
            },
          })).then(res => {
            dispatch({
                type: BACKTEST,
                payload: res.data
            });
        }).catch(err => {
            stopLoading();
            setError(err.message, "danger");
        });
    };

    const signup = (data) => {
        setLoading();
        getToken().then(token => axios.post(`${base_url}/auth/signup`,data, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': token
            },
          })).then(res => {
            dispatch({
                type: SIGNUP,
                payload: res.data
            });
        }).catch(err => {
            stopLoading();
            setError(err.message, "danger");
        });
    };

    const login = (data) => {
        console.log(data)
        setLoading();
        getToken().then(token => axios.post(`${base_url}/auth/login`,data, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': token
            },
          })).then(res => {
            console.log(res.data)
            localStorage.setItem("token",res.data.token)
            dispatch({
                type: LOGIN,
                payload: res.data
            });
        }).catch(err => {
            stopLoading();
            setError(err.message, "danger");
        });
    };

    const logout = () => {
        console.log("logout")
        setLoading();
        dispatch({
                type: LOGOUT
            });
        localStorage.removeItem("token")
    }

    return (
        <DataContext.Provider value={{
            tickers:state.tickers,
            strategies:state.strategies,
            descriptions:state.descriptions,
            results:state.results,
            loading:state.loading,
            error:state.error,
            title:state.title,
            text:state.text,
            login:state.login,
            logout:state.logout,
            isAuth:state.isAuth,
            authToken:state.authToken,
            user:state.user,
            login,
            logout,
            signup,
            getTickers,
            getStrategy,
            getDescription,
            backtest,
        }}>
            {props.children}
        </DataContext.Provider>
    )
}

export default DataState;