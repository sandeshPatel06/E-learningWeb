import React from 'react';

function PasswordResetComplete({ navigate }) {
  return (
    <div className="flex flex-col items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200 w-full max-w-md text-center">
        <h1 className="text-4xl font-bold mb-6 text-blue-800">Password Reset Complete</h1>
        <p className="text-gray-700 mb-6">
          Your password has been set. You may now log in with your new password.
        </p>
        <button
          onClick={() => navigate('/login')}
          className="btn btn-primary bg-blue-900 text-white hover:bg-blue-700 px-6 py-3"
        >
          Log in
        </button>
      </div>
    </div>
  );
}

export default PasswordResetComplete;
