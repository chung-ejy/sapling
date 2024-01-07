import { LOGIN, LOGOUT, SIGNUP, GET_TICKERS,  GET_STRATEGY, GET_DESCRIPTION, BACKTEST, SET_LOADING, SET_ERROR, CLEAR_ERROR } from "./types";
const Reducer = (state,action) => {
    switch(action.type) {
        case SET_ERROR:
            return {
                ...state,
                error: {msg:"rekt",type:"big sadge"},
            }
        case CLEAR_ERROR:
            return {
                ...state,
                error:null
            }
        case SET_LOADING:
            return {
                ...state,
                loading:true
            }
        case GET_STRATEGY:
            return {
                ...state,
                strategies:action.payload,
                loading:false
            }
        case GET_TICKERS:
            return {
                ...state,
                tickers:action.payload,
                loading:false
            }
        case GET_DESCRIPTION:
            return {
                ...state,
                descriptions:action.payload,
                loading:false
            }
        case BACKTEST:
            return {
                ...state,
                results:action.payload,
                loading:false
            }
        case SIGNUP:
            return {
                ...state,
                loading:false
            }
        case LOGIN:
            return {
                ...state,
                isAuth:true,
                user:action.payload.user,
                loading:false
            }
        case LOGOUT:
                return {
                    ...state,
                    isAuth:false,
                    user:{},
                    loading:false
                }
        default:
            return {
                ...state,
            }
    }
}

export default Reducer