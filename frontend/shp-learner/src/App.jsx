import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home'; // Create this component
import Login from './pages/Login'; // Create this component
import Register from './pages/Register'; // Create this component
import Profile from './pages/Profile'; // Create this component
import CourseDetail from './pages/CourseDetail'; // Create this component
import Enroll from './pages/Enroll'; // Create this component
import FAQ from './pages/FAQ'; // Create this component

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/courses/:slug" element={<CourseDetail />} />
          <Route path="/enroll/:slug" element={<Enroll />} />
          <Route path="/faq" element={<FAQ />} />
          {/* Add more routes as you convert pages */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;