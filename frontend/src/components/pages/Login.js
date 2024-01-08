import React from 'react';
import LoginForm from "../forms/LoginForm"
import SignupForm from '../forms/SignupForm';

const Login = () => {
    return (
        <div className="container">
            <LoginForm />
            <SignupForm />
        </div>
    )
}

export default Login