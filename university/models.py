from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="card")
    card_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Card #{self.card_number} - {self.student}"


class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Prof. {self.first_name} {self.last_name}"


class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CourseDescription(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] + "..."


class Course(models.Model):
    title = models.CharField(max_length=200)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="courses")
    students = models.ManyToManyField(Student, related_name="courses", blank=True)
    description = models.OneToOneField(CourseDescription, on_delete=models.CASCADE, related_name="course")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.title} ({self.semester})"   