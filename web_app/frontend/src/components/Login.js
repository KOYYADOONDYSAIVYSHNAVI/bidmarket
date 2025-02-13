import React, { useState } from 'react';
import { useNavigate, Link, useParams } from 'react-router-dom'; 
import userService from '../services/userService';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); 
  const user_id = useParams();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await userService.login({ email, password });
  
      if (response.token && response.user_id) {
        localStorage.setItem('token', response.token); 
        navigate(`/bidding/${response.user_id}`); 
      } else {
        setError('Login failed. Please check your credentials.');
      }
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    }
  };
  

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p>{error}</p>}
        <button type="submit">Login</button>
      </form>

      <div>
        {/* Link to Sign Up page */}
        <p>
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
