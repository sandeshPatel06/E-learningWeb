// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import App from './App.jsx';

// // Create a root and render the App component into it
// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
// );


// src/index.js (or main.jsx)
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; // Now import App from App.jsx
// import './index.css'; // Your main CSS file, likely for Tailwind CSS

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);