from rest_framework import serializers
from .models import CustomUser, Category, Course, Lesson, Enrollment, Quiz, FAQ

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Includes all fields.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'bio', 'profile_picture']

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Includes all fields.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    Includes all fields.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    Includes nested serializers for instructor (CustomUser) and category.
    Also includes lessons for the course.
    """
    instructor = CustomUserSerializer(read_only=True) # Read-only as it's a nested object
    category = CategorySerializer(read_only=True) # Read-only as it's a nested object
    lessons = LessonSerializer(many=True, read_only=True) # Nested lessons, many-to-one relationship

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'instructor', 'category',
                  'created_at', 'updated_at', 'price', 'is_free', 'lessons']

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.
    Includes nested serializers for student (CustomUser) and course.
    """
    student = CustomUserSerializer(read_only=True) # Read-only
    course = CourseSerializer(read_only=True) # Read-only

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'progress']

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quiz model.
    Includes all fields.
    """
    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'created_at'] # 'lesson' will be its ID by default

class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQ model.
    Includes all fields.
    """
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at']
