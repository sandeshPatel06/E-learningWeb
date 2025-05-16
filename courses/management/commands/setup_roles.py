from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import CustomUser, Course, Lesson, Quiz, Enrollment

class Command(BaseCommand):
    help = 'Set up groups and assign permissions for user roles'

    def handle(self, *args, **kwargs):
        # Define content types
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        quiz_ct = ContentType.objects.get_for_model(Quiz)
        enrollment_ct = ContentType.objects.get_for_model(Enrollment)

        # Define groups and their permissions
        groups = {
            'Student': [
                ('view_course', course_ct),
                ('view_lesson', lesson_ct),
                ('view_quiz', quiz_ct),
                ('view_enrollment', enrollment_ct),
                ('add_enrollment', enrollment_ct),
            ],
            'Instructor': [
                ('add_course', course_ct),
                ('change_course', course_ct),
                ('delete_course', course_ct),
                ('view_course', course_ct),
                ('add_lesson', lesson_ct),
                ('change_lesson', lesson_ct),
                ('delete_lesson', lesson_ct),
                ('view_lesson', lesson_ct),
                ('add_quiz', quiz_ct),
                ('change_quiz', quiz_ct),
                ('delete_quiz', quiz_ct),
                ('view_quiz', quiz_ct),
            ],
            'Admin': []  # Will be assigned all permissions
        }

        # Setup groups
        for group_name, perms in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(f"Group already exists: {group_name}")

            group.permissions.clear()

            if group_name == 'Admin':
                group.permissions.set(Permission.objects.all())
                self.stdout.write(f"Assigned ALL permissions to {group_name}")
            else:
                for codename, ct in perms:
                    try:
                        perm = Permission.objects.get(codename=codename, content_type=ct)
                        group.permissions.add(perm)
                        self.stdout.write(f"Added {codename} to {group_name}")
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permission {codename} not found for {ct}"))

        self.stdout.write(self.style.SUCCESS("Group and permission setup complete."))
