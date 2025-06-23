import React from 'react';

function Enroll({ course, user, addEnrollment, navigate }) {
  if (!user) {
    // Should ideally be handled by App.jsx routing, but as a fallback:
    return <p className="text-center text-xl mt-10">Please log in to enroll in courses.</p>;
  }

  if (!course) {
    return <p className="text-center text-xl mt-10">Course not found.</p>;
  }

  const handleConfirmEnrollment = (e) => {
    e.preventDefault();
    const enrolled = addEnrollment(user, course);
    if (enrolled) {
      alert(`You have successfully enrolled in ${course.title}!`); // Using alert temporarily for user feedback
      navigate(`/course/${course.slug}`);
    } else {
      alert(`You are already enrolled in ${course.title}.`); // Using alert temporarily for user feedback
      navigate(`/course/${course.slug}`);
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200 max-w-md mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-4 text-blue-800">Enroll in {course.title}</h1>
      <p className="text-gray-700 mb-4">
        You are about to enroll in <strong className="font-semibold">{course.title}</strong>.
      </p>
      <p className="text-gray-700 mb-6">
        <strong className="font-semibold">Price:</strong>{' '}
        {course.is_free ? 'Free' : `₹${course.price}`}
      </p>

      <form onSubmit={handleConfirmEnrollment}>
        <div className="flex justify-between space-x-4">
          <button type="submit" className="btn btn-primary flex-1">
            Confirm Enrollment
          </button>
          <button
            type="button"
            onClick={() => navigate(`/course/${course.slug}`)}
            className="btn btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default Enroll;
