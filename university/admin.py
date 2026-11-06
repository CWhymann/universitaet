from django.contrib import admin
from .models import Student, StudentCard, Professor, Semester, CourseDescription, Course


class StudentCardInline(admin.TabularInline):
    model = StudentCard


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "professor", "semester")


admin.site.register(Student, inlines=[StudentCardInline])
admin.site.register(StudentCard)
admin.site.register(Professor)
admin.site.register(Semester)
admin.site.register(CourseDescription)
admin.site.register(Course, CourseAdmin)   