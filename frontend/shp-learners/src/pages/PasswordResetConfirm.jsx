import React, { useState } from 'react';

function PasswordResetConfirm({ navigate }) {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // In a real app, uidb64 and token would be extracted from the URL (e.g., via React Router)
  // For this simulation, we'll just show the form.

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (newPassword.length < 6) {
      setError('New password must be at least 6 characters long.');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    // Simulate password change
    // In a real application, you would make an API call to your backend
    console.log('Simulating password change for user with new password.');
    setMessage('Your password has been successfully reset.');

    setTimeout(() => {
      navigate('/password_reset/complete'); // Navigate to the complete page
    }, 1500);
  };

  return (
    <div className="flex flex-col items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200 w-full max-w-md">
        <h1 className="text-4xl font-bold mb-6 text-center text-blue-800">Set New Password</h1>
        <p className="text-gray-700 mb-6 text-center">
          Please enter your new password below.
        </p>

        {message && (
          <div className="alert alert-success bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-4" role="alert">
            {message}
          </div>
        )}
        {error && (
          <div className="alert alert-error bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="w-full">
          <div className="form-group">
            <label htmlFor="new_password" className="form-label">New Password</label>
            <input
              type="password"
              name="new_password"
              id="new_password"
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-800"
              required
              autoComplete="new-password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirm_password" className="form-label">Confirm New Password</label>
            <input
              type="password"
              name="confirm_password"
              id="confirm_password"
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-800"
              required
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary bg-blue-900 text-white hover:bg-blue-700 w-full py-3 mt-4">
            Reset Password
          </button>
        </form>
      </div>
    </div>
  );
}

export default PasswordResetConfirm;
