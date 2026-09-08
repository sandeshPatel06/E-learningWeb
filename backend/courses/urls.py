from django.urls import path
from .api_views import (
    CustomUserListCreateAPIView, CustomUserRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView,
    LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView,
    EnrollmentListCreateAPIView, EnrollmentRetrieveUpdateDestroyAPIView,
    QuizListCreateAPIView, QuizRetrieveUpdateDestroyAPIView,
    FAQListCreateAPIView, FAQRetrieveUpdateDestroyAPIView,
    LoginAPIView, RegisterAPIView,
)

urlpatterns = [
    # CustomUser API URLs
    path('users/', CustomUserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Category API URLs
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),

    # Course API URLs
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),

    # Lesson API URLs
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),

    # Enrollment API URLs
    path('enrollments/', EnrollmentListCreateAPIView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', EnrollmentRetrieveUpdateDestroyAPIView.as_view(), name='enrollment-detail'),

    # Quiz API URLs
    path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyAPIView.as_view(), name='quiz-detail'),

    # FAQ API URLs
    path('faqs/', FAQListCreateAPIView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQRetrieveUpdateDestroyAPIView.as_view(), name='faq-detail'),

    # Login and Registration API URLs
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
]