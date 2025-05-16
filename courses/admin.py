from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Course, Lesson, Enrollment

from django.contrib import admin
from .models import FAQ


# Inline for Lessons within Course admin
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'video_url', 'content')
    ordering = ('order',)

# CustomUser admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')  # horizontal filter for M2M

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Course admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'is_free', 'created_at')
    list_filter = ('category', 'is_free', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    list_editable = ('is_free',)
    date_hierarchy = 'created_at'

# Lesson admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    list_editable = ('order',)
    ordering = ('course', 'order')

# Enrollment admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
    list_editable = ('progress',)
    date_hierarchy = 'enrolled_at'

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')


admin.site.register(FAQ, FAQAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
