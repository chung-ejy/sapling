import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const submitLoginForm = async () => {
    try {
      const response = await axios.post('http://yourbackend/api/auth/login/', {
        username,
        password,
      });

      // Handle the response and token storage
      console.log(response.data);

    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="card">
        <div className="card-body">
          <h2 className="card-title">Login</h2>
          <form>
            <div className="mb-3">
              <label htmlFor="username" className="form-label">Username:</label>
              <input
                type="text"
                className="form-control"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="mb-3">
              <label htmlFor="password" className="form-label">Password:</label>
              <input
                type="password"
                className="form-control"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button type="button" className="btn btn-primary" onClick={submitLoginForm}>
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
