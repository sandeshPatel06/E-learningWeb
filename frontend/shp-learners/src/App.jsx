import React, { useState, useEffect, createContext } from 'react';
import BaseLayout from './components/BaseLayout.jsx';
import Router from './router.jsx'; // <- Import new Router

export const UserContext = createContext(null);

function App() {
  const [currentRoute, setCurrentRoute] = useState(window.location.pathname);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    const handlePopState = () => setCurrentRoute(window.location.pathname);
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (path) => {
    window.history.pushState({}, '', path);
    setCurrentRoute(path);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('currentUser', JSON.stringify(userData));
    navigate('/');
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('currentUser');
    navigate('/');
  };

  const mockCourses = [/* ...same as before... */];

  const [mockEnrollments, setMockEnrollments] = useState(() => {
    const stored = localStorage.getItem('mockEnrollments');
    return stored ? JSON.parse(stored) : [];
  });

  useEffect(() => {
    localStorage.setItem('mockEnrollments', JSON.stringify(mockEnrollments));
  }, [mockEnrollments]);

  const addEnrollment = (student, course) => {
    const exists = mockEnrollments.some(e => e.student.username === student.username && e.course.slug === course.slug);
    if (!exists) {
      const newEnrollment = { student, course, progress: 0 };
      setMockEnrollments(prev => [...prev, newEnrollment]);
      return true;
    }
    return false;
  };

  return (
    <UserContext.Provider value={{ user, setUser, handleLogin, handleLogout, navigate }}>
      <BaseLayout user={user} onLogout={handleLogout} navigate={navigate}>
        <Router
          currentRoute={currentRoute}
          user={user}
          courses={mockCourses}
          enrollments={mockEnrollments}
          onLogin={handleLogin}
          navigate={navigate}
          addEnrollment={addEnrollment}
        />
      </BaseLayout>
    </UserContext.Provider>
  );
}

export default App;
