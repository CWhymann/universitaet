from django.db import models
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Professor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professor_profile",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="professors",
    )
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.title})"


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students",
    )
    matriculation_number = models.CharField(max_length=20, unique=True)
    enrolled_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.matriculation_number} – {self.user.get_full_name()}"


class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses",
    )
    credits = models.PositiveSmallIntegerField(default=5)
    semester = models.CharField(max_length=10)
    professors = models.ManyToManyField(
        Professor,
        through="TeachingAssignment",
        related_name="courses_taught",
    )

    def __str__(self):
        return f"{self.code} – {self.title}"


class TeachingAssignment(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[("lead", "Lehrende:r"), ("assistant", "Mitwirkende:r")],
        default="lead",
    )

    class Meta:
        unique_together = ("professor", "course")


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("enrolled", "Eingeschrieben"),
            ("completed", "Bestanden"),
            ("failed", "Nicht bestanden"),
        ],
        default="enrolled",
    )
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")


class Exam(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="exams",
    )
    date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.course.code} – {self.date:%Y-%m-%d}"   

# Create your models here.
