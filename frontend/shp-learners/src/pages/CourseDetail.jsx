import React from 'react';

function CourseDetail({ course, isEnrolled, user, navigate }) {
  if (!course) {
    return <p className="text-center text-xl mt-10">Course not found.</p>;
  }

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200">
      <h1 className="text-4xl font-bold mb-4 text-blue-800">{course.title}</h1>
      <p className="text-gray-700 mb-4">{course.description}</p>
      <p className="text-gray-700 mb-2">
        <strong className="font-semibold">Instructor:</strong> {course.instructor.username}
      </p>
      <p className="text-gray-700 mb-2">
        <strong className="font-semibold">Category:</strong> {course.category.name}
      </p>
      <p className="text-gray-700 mb-4">
        <strong className="font-semibold">Price:</strong>{' '}
        {course.is_free ? 'Free of Cost' : `₹${course.price}`}
      </p>
      <p className="text-gray-600 text-sm mb-6">
        <strong className="font-semibold">Created:</strong> {new Date(course.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
      </p>

      {user ? (
        isEnrolled ? (
          <>
            <p className="text-green-600 font-bold mb-4">You are enrolled in this course!</p>
            <button className="btn btn-primary bg-green-600 text-white cursor-not-allowed opacity-75" disabled>
              Enrolled
            </button>
          </>
        ) : (
          <button
            onClick={() => navigate(`/enroll/${course.slug}`)}
            className="btn btn-primary bg-blue-600 text-white hover:bg-blue-700"
          >
            Enroll Now
          </button>
        )
      ) : (
        <p className="text-gray-700 mt-4">
          Please{' '}
          <button onClick={() => navigate('/login')} className="text-blue-600 hover:underline">
            log in
          </button>{' '}
          to enroll in this course.
        </p>
      )}

      {isEnrolled && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Lessons</h2>
          {course.lessons && course.lessons.length > 0 ? (
            <ul className="list-group">
              {course.lessons.map((lesson) => (
                <li key={lesson.order} className="list-group-item">
                  <span className="font-semibold text-gray-800">{lesson.title}</span>{' '}
                  <span className="text-gray-600">(Lesson {lesson.order})</span>
                  {lesson.video_url && (
                    <a
                      href={lesson.video_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline ml-4"
                    >
                      Watch Video
                    </a>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p className="list-group-item text-gray-600">No lessons available yet.</p>
          )}
        </div>
      )}

      {!isEnrolled && (
        <p className="alert alert-warning mt-8">
          You need to enroll in this course to access the lessons.
        </p>
      )}
    </div>
  );
}

export default CourseDetail;
