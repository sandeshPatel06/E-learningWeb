// CourseDetailWrapper.jsx
import { useParams } from 'react-router-dom';
import CourseDetail from './pages/CourseDetail.jsx';

export function CourseDetailWrapper({ courses, enrollments, user, navigate }) {
  const { slug } = useParams();
  const course = courses.find(c => c.slug === slug);
  const isEnrolled = user
    ? enrollments.some(e => e.student.username === user.username && e.course.slug === slug)
    : false;

  return course
    ? <CourseDetail course={course} isEnrolled={isEnrolled} user={user} navigate={navigate} />
    : <p className="text-center text-xl mt-10">Course not found.</p>;
}

// EnrollWrapper.jsx
import { useParams } from 'react-router-dom';
import Enroll from './pages/Enroll.jsx';
import Login from './pages/Login.jsx';

export function EnrollWrapper({ courses, user, navigate, addEnrollment, onLogin }) {
  const { slug } = useParams();
  const course = courses.find(c => c.slug === slug);

  return user && course
    ? <Enroll course={course} user={user} addEnrollment={addEnrollment} navigate={navigate} />
    : <Login onLogin={onLogin} navigate={navigate} />;
}
