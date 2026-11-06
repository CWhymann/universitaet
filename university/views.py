from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Course, Enrollment, Student, Professor


def dashboard(request):
    departments = Department.objects.all()
    courses = Course.objects.select_related("department").prefetch_related("professors")
    return render(request, "university/dashboard.html", {
        "departments": departments,
        "courses": courses,
    })


def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related("department"), pk=pk
    )
    enrollments = course.enrollments.select_related("student__user")
    return render(request, "university/course_detail.html", {
        "course": course,
        "enrollments": enrollments,
    })   

# Create your views here.
