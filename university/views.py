from django.shortcuts import render
from .models import Student, Professor, Course, Semester


def index(request):
    return render(request, "university/index.html", {
        "students": Student.objects.count(),
        "professors": Professor.objects.count(),
        "courses": Course.objects.count(),
        "semesters": Semester.objects.count(),
    })   