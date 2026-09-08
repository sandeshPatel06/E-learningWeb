import React from 'react';

function PasswordResetDone({ navigate }) {
  return (
    <div className="flex flex-col items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200 w-full max-w-md text-center">
        <h1 className="text-4xl font-bold mb-6 text-blue-800">Password Reset Email Sent</h1>
        <p className="text-gray-700 mb-4">
          We've emailed you instructions for setting your password, if an account exists with the email you entered.
          You should receive them shortly.
        </p>
        <p className="text-gray-700 mb-6">
          If you don't receive an email, please make sure you've entered the address you registered with,
          and check your spam folder.
        </p>
        <button
          onClick={() => navigate('/login')}
          className="btn btn-primary bg-blue-900 text-white hover:bg-blue-700 px-6 py-3"
        >
          Return to Login
        </button>
      </div>
    </div>
  );
}

export default PasswordResetDone;
