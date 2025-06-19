import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Layout.css'; // Assuming you move your base.html CSS here
import logo from '../assets/logo.png'; // Assuming logo.png is in src/assets

const Layout = ({ children }) => {
  const [isNavActive, setIsNavActive] = useState(false);

  const toggleNav = () => {
    setIsNavActive(!isNavActive);
  };

  // This would typically come from a global state or context in a real app
  const user = {
    isAuthenticated: true, // Replace with actual auth check
    isStaff: false, // Replace with actual staff check
    username: 'JohnDoe', // Example
  };

  return (
    <>
      {/* Navbar */}
      <nav className="navbar" aria-label="Main navigation">
        <div className="container">
          <Link className="navbar-brand" to="/">
            <img src={logo} alt="Logo" className="navbar-logo" />
            SHP-Learner
          </Link>
          <button
            className="navbar-toggle"
            aria-label="Toggle navigation"
            onClick={toggleNav}
          >
            ☰
          </button>
          <ul className={`navbar-nav ${isNavActive ? 'active' : ''}`} id="navbarNav">
            <li><Link to="/">Home</Link></li>
            {/* <li><Link to="/courses">Courses</Link></li> */}

            {user.isAuthenticated ? (
              <>
                {!user.isStaff && (
                  <li><Link to="/profile">Profile</Link></li>
                )}
                <li><Link to="/logout">Logout</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/login">Login</Link></li>
                {/* <li><Link to="/register">Register</Link></li> */}
              </>
            )}

            {user.isStaff && (
              <li><a href="/admin">Admin</a></li>
            )}
          </ul>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container">{children}</main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container container">
          <div className="footer-about">
            <h4>About Us</h4>
            <p>SHP-Learnering Platform is dedicated to providing high-quality courses to help you enhance your skills and achieve your career goals. Join us to start learning today!</p>
          </div>
          <div className="footer-links">
            <h4>Quick Links</h4>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><a href="https://wa.me/9399613606">Contact Us</a></li>
              <li><Link to="/faq">FAQ</Link></li>
            </ul>
          </div>
          <div className="footer-contact">
            <h4>Contact Us</h4>
            <p><i className="fas fa-envelope"></i> sandeshpatel.sp.93@gmail.com</p>
            <p><i className="fas fa-phone-alt"></i> +91 9399613606</p>
            <p><i className="fas fa-map-marker-alt"></i> 420 Kareli St, MP Narsinghpur, India</p>
          </div>
          <div className="footer-social">
            <h4>Follow Us</h4>
            <div className="social-icons">
              <a href="https://x.com/SandeshPat007?t=teYEP7w9aNZYSYKc0sF7dQ&s=09" className="social-icon" target="_blank" rel="noopener noreferrer"><i className="fab fa-twitter"></i></a>
              <a href="https://www.linkedin.com/in/sandesh-patel07" className="social-icon" target="_blank" rel="noopener noreferrer"><i className="fab fa-linkedin-in"></i></a>
              <a href="https://www.instagram.com/sandesh_patel007" className="social-icon" target="_blank" rel="noopener noreferrer"><i className="fab fa-instagram"></i></a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 SHP-Learnering Platform. All Rights Reserved |
            <Link to="#">Privacy Policy</Link> |
            <Link to="#">Terms of Service</Link>
          </p>
        </div>
      </footer>
    </>
  );
};

export default Layout;