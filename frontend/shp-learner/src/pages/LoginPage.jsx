// src/pages/LoginPage.jsx
import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext'; // You'll create this

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useContext(AuthContext); // Get login function from context
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        try {
            // Replace with your actual API call to your backend for login
            const response = await fetch('/api/login/', { // Assuming a Django REST API endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                login(data.token, data.user); // Store token and user info (e.g., in localStorage and context)
                navigate('/profile'); // Redirect to profile page on successful login
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Invalid username or password. Please try again.');
            }
        } catch (err) {
            setError('An error occurred. Please try again later.');
            console.error('Login error:', err);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: 'auto', padding: '20px' }}>
            <h1>Login</h1>

            {error && (
                <p className="form-error" role="alert" id="form-errors">
                    {error}
                </p>
            )}

            <form onSubmit={handleSubmit} aria-describedby="form-errors">
                <div className="form-group">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        name="username"
                        id="username"
                        className="form-control"
                        required
                        autoComplete="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        className="form-control"
                        required
                        autoComplete="current-password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div className="form-actions" style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginTop: '15px'
                }}>
                    <Link to="/password-reset" className="btn btn-link">Forgot password?</Link>
                    <button type="submit" className="btn btn-primary" style={{
                        padding: '10px 20px',
                        borderRadius: '4px',
                        textDecoration: 'none',
                        display: 'inline-block',
                        textAlign: 'center',
                        color: 'white',
                        border: 'none',
                    }}>Login</button>
                </div>
            </form>

            <p style={{ marginTop: '20px' }}>
                Don't have an account?
                <Link to="/register">Register here</Link>
            </p>
        </div>
    );
};

export default LoginPage;