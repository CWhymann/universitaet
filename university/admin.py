from django.contrib import admin
from .models import (
    Department,
    Professor,
    Student,
    Course,
    TeachingAssignment,
    Enrollment,
    Exam,
)


class TeachingAssignmentInline(admin.TabularInline):
    model = TeachingAssignment


class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "semester", "credits")
    inlines = [TeachingAssignmentInline]


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


class CourseAdminWithEnrollments(admin.ModelAdmin):
    list_display = ("code", "title", "department", "semester", "credits")
    inlines = [TeachingAssignmentInline, EnrollmentInline]


admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Course, CourseAdminWithEnrollments)
admin.site.register(Enrollment)
admin.site.register(Exam)   

# Register your models here.
