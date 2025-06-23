from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    is_email_verified = models.BooleanField(default=False)
    # date_joined is already inherited from AbstractUser

    highest_qualification = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills like Python, ML, etc.")

    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='following_users') # Renamed related_name to avoid conflict
    # 'courses.Course' needs to refer to the actual app name where Course model is defined
    # Assuming 'courses' is the app name, this is correct. If not, change 'courses'
    bookmarks = models.ManyToManyField('Course', blank=True, related_name='bookmarked_by') 
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_students_via_m2m') # Renamed related_name
    completed_courses = models.ManyToManyField('Course', blank=True, related_name='completed_students_via_m2m') # Renamed related_name
    
    quiz_scores = models.JSONField(blank=True, null=True, help_text="Store quiz scores or progress data")

    instructor_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_active_user = models.BooleanField(default=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    login_ip = models.GenericIPAddressField(null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)

    class Meta:
        # Avoid duplicate CustomUser declaration
        pass 

    def __str__(self):
        return f"{self.username} ({self.role})"

    # The save method was commented out, keep it that way if it's not needed,
    # otherwise uncomment and ensure it doesn't conflict with AbstractUser's save logic
    # def save(self, *args, **kwargs):
    #     if self.role in ['instructor', 'admin']:
    #         self.is_staff = True
    #     else:
    #         self.is_staff = False
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    short_description = models.CharField(max_length=500, help_text="A brief overview of the course.")
    description = models.TextField(help_text="Detailed course description, including learning objectives.")
    what_you_will_learn = models.TextField(blank=True, null=True, help_text="Comma-separated or bullet points of learning outcomes.")
    requirements = models.TextField(blank=True, null=True, help_text="Prerequisites or materials needed for the course.")
    target_audience = models.TextField(blank=True, null=True, help_text="Who is this course for?")

    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='taught_courses', limit_choices_to={'role__in': ['instructor', 'admin']}) # Allow admin to be instructor
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')

    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True, help_text="Thumbnail image for the course listing.")
    promo_video_url = models.URLField(blank=True, null=True, help_text="Link to a promotional video for the course.")

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False, help_text="Set to true to make the course visible to users.")
    level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner')

    duration = models.CharField(max_length=50, blank=True, null=True, help_text="E.g., '10 hours', '3 weeks'")
    total_lectures = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(5)])
    number_of_reviews = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250) # Removed unique=True here, as unique_together handles it
    content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Direct URL to video or embed link.")
    order = models.PositiveIntegerField(help_text="Order of the lesson within the course.")
    is_preview = models.BooleanField(default=False, help_text="Can this lesson be previewed by non-enrolled users?")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Ensure slug is unique for this course, but not globally unique
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Lesson.objects.filter(course=self.course, slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.order}. {self.title}"

    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'course_slug': self.course.slug, 'lesson_slug': self.slug})


class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    progress = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, help_text="Optional description for the quiz.")
    passing_score = models.PositiveIntegerField(default=70, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Percentage required to pass the quiz.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz: {self.title} for {self.lesson.title}"

    class Meta:
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('mcq', 'Multiple Choice'), ('text', 'Text Answer')], default='mcq')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question_text[:75]

    class Meta:
        ordering = ['order']

class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text[:75]


class UserQuizAttempt(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts', limit_choices_to={'role': 'student'})
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
    passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} (Score: {self.score}%)"

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('student', 'quiz', 'attempt_number')


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    unique_id = models.CharField(max_length=100, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            import uuid
            self.unique_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate for {self.enrollment.student.username} - {self.enrollment.course.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given', limit_choices_to={'role': 'student'})
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating out of 5 stars.")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval for review visibility.")

    class Meta:
        unique_together = ('course', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.course.title} by {self.student.username} - {self.rating} stars"


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:60] + "..." if len(self.question) > 60 else self.question

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['order']