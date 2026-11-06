from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
]   