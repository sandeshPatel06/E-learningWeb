import React, { useEffect, useState } from 'react';
import Home from './pages/Home.jsx';
import CourseDetail from './pages/CourseDetail.jsx';
import Enroll from './pages/Enroll.jsx';
import FAQ from './pages/FAQ.jsx';
import Login from './pages/Login.jsx';
import Profile from './pages/Profile.jsx';
import Register from './pages/Register.jsx';
import PasswordReset from './pages/PasswordReset.jsx';
import PasswordResetDone from './pages/PasswordResetDone.jsx';
import PasswordResetConfirm from './pages/PasswordResetConfirm.jsx';
import PasswordResetComplete from './pages/PasswordResetComplete.jsx';

export default function Router({
  currentRoute,
  user,
  courses: initialCourses,
  enrollments: initialEnrollments,
  onLogin,
  navigate,
  addEnrollment
}) {
  const [courses, setCourses] = useState(initialCourses || []);
  const [enrollments, setEnrollments] = useState(initialEnrollments || []);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch('http://localhost:8000/api/courses/')
      .then(res => res.json())
      .then(data => setCourses(data))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (user) {
      fetch('http://localhost:8000/api/enrollments/', { credentials: 'include' })
        .then(res => res.json())
        .then(data => setEnrollments(data));
    } else {
      setEnrollments([]);
    }
  }, [user]);

  const pathSegments = currentRoute.split('/').filter(Boolean);

  // Redirect helper component to avoid calling navigate in render
  function Redirect({ to }) {
    useEffect(() => {
      navigate(to);
    }, [to]);
    return null;
  }

  // Use Redirect component for '/courses'
  if (pathSegments[0] === 'courses') {
    return <Redirect to="/" />;
  }

  // Helper functions for route matching
  const isHome = pathSegments.length === 0 || pathSegments[0] === 'index';
  const isCourseDetail = pathSegments[0] === 'course' && pathSegments[1];
  const isProfile = pathSegments[0] === 'profile';
  const isLogin = pathSegments[0] === 'login';
  const isRegister = pathSegments[0] === 'register';
  const isEnroll = pathSegments[0] === 'enroll' && pathSegments[1];
  const isFAQ = pathSegments[0] === 'faq';
  const isPasswordReset = pathSegments[0] === 'password_reset';

  if (isHome) {
    return <Home courses={courses} navigate={navigate} />;
  }

  if (isCourseDetail) {
    const slug = pathSegments[1];
    const course = courses.find(c => c.slug === slug);
    const isEnrolled = user
      ? enrollments.some(e => e.student.username === user.username && e.course.slug === slug)
      : false;
    return course
      ? <CourseDetail course={course} isEnrolled={isEnrolled} user={user} navigate={navigate} />
      : <p className="text-center text-xl mt-10">Course not found.</p>;
  }

  if (isProfile) {
    const userEnrollments = user
      ? enrollments.filter(e => e.student.username === user.username)
      : [];
    return user
      ? <Profile user={user} enrollments={userEnrollments} navigate={navigate} />
      : <Login onLogin={onLogin} navigate={navigate} />;
  }

  if (isLogin) {
    return <Login onLogin={onLogin} navigate={navigate} />;
  }

  if (isRegister) {
    return <Register navigate={navigate} />;
  }

  if (isEnroll) {
    const slug = pathSegments[1];
    const course = courses.find(c => c.slug === slug);
    return user && course
      ? <Enroll course={course} user={user} addEnrollment={addEnrollment} navigate={navigate} />
      : <Login onLogin={onLogin} navigate={navigate} />;
  }

  if (isFAQ) {
    return <FAQ />;
  }

  if (isPasswordReset) {
    if (pathSegments[1] === 'done') {
      return <PasswordResetDone navigate={navigate} />;
    } else if (pathSegments[1] && pathSegments[2]) {
      return <PasswordResetConfirm navigate={navigate} />;
    } else if (pathSegments[1] === 'complete') {
      return <PasswordResetComplete navigate={navigate} />;
    }
    return <PasswordReset navigate={navigate} />;
  }

  // Default fallback
  return <Home courses={courses} navigate={navigate} />;
}
