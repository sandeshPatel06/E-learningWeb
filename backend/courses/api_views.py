from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import CustomUser, Category, Course, Lesson, Enrollment, Quiz, FAQ
from .serializers import (
    CustomUserSerializer, CategorySerializer, CourseSerializer,
    LessonSerializer, EnrollmentSerializer, QuizSerializer, FAQSerializer
)

# import traceback
from .utils.mail import trigger_email  
import os
import traceback

# --- CustomUser API Views ---
class CustomUserListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all CustomUsers or create a new CustomUser.
    Allows any user to create (for registration), but only authenticated to list.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny] # Allow anyone to register (create), but restrict list if needed
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class CustomUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific CustomUser by ID.
    Only authenticated users can access.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated] # Typically, only owner or admin should update/delete
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def patch(self, request, *args, **kwargs):
        # Only allow users to edit their own profile, or admin
        user = self.get_object()
        if request.user != user and not request.user.is_superuser:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)


# --- Category API Views ---
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all Categories or create a new Category.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Adjust permissions as needed (e.g., IsAdminUser)

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Adjust permissions as needed (e.g., IsAdminUser)


# --- Course API Views ---
class CourseListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all Courses or create a new Course.
    """
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny] # Allow anyone to view, but restrict create to instructors/admins

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Course by ID.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny] # Allow anyone to view, but restrict update/delete to instructors/admins


# --- Lesson API Views ---
class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all Lessons or create a new Lesson.
    """
    queryset = Lesson.objects.all().order_by('order')
    serializer_class = LessonSerializer
    permission_classes = [AllowAny] # Adjust permissions (e.g., IsAuthenticated, IsAdminUser)

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Lesson by ID.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny] # Adjust permissions


# --- Enrollment API Views ---
class EnrollmentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all Enrollments or create a new Enrollment.
    Anyone can list, only authenticated users can create.
    """
    serializer_class = EnrollmentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        # For GET, return all enrollments (or filter as needed)
        user = self.request.user
        # print(Enrollment.objects.filter(student=user).order_by('-created_at'))
        print(user, "is requesting enrollments")
        return Enrollment.objects.all().order_by('-enrolled_at')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class EnrollmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Enrollment by ID.
    Only authenticated users (typically the student or an admin) can access.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# --- Quiz API Views ---
class QuizListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all Quizzes or create a new Quiz.
    """
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    permission_classes = [AllowAny] # Adjust permissions

class QuizRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Quiz by ID.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny] # Adjust permissions


# --- FAQ API Views ---
class FAQListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all FAQs or create a new FAQ.
    """
    queryset = FAQ.objects.all().order_by('-created_at')
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]

class FAQRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific FAQ by ID.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]


# --- Login API View ---
class LoginAPIView(APIView):
    """
    API endpoint for logging in a user using username and password.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# --- Register API View ---
class RegisterAPIView(APIView):
    """
    API endpoint for registering a new user.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'student')

        # Basic validation
        if not username or not email or not password:
            return Response({'message': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'message': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        is_staff = True if role == 'instructor' else False
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff
        )
        user.save()

        # --- Send Welcome Email ---
        try:
            # Log important user info and environment variables for debug purposes
            print(f"Preparing to send welcome email to: {user.email}")
            print(f"Username: {user.username}")
            
        
            welcome_context = {
                'user': user,
                            }
        
            welcome_email_template = 'welcome_email.html'
            welcome_email_subject = f'Welcome to SHP-Learner, {user.username}!'
        
            email_error = trigger_email(
                context=welcome_context,
                template=welcome_email_template,
                subject=welcome_email_subject,
                recipients=[user.email],
                message=f"Welcome to SHP-Learner, {user.username}! We're excited to have you."
            )
        
            if email_error:
                print(f"[Email Error] Failed to send welcome email to1212 {user.email}: {email_error}")
                print(email_error)
        
        except Exception as e:
            print("[Exception] Unexpected error when trying to send welcome email:")
            traceback.print_exc()
        
        # --- End Send Welcome Email ---
        
        return Response({'message': 'Registration successful!'}, status=status.HTTP_201_CREATED)