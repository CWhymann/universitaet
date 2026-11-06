from university.models import *

s1 = Semester.objects.create(name="Sommersemester 2026")
s2 = Semester.objects.create(name="Wintersemester 2026")

p1 = Professor.objects.create(first_name="Anna", last_name="Mueller", email="mueller@uni.de")
p2 = Professor.objects.create(first_name="Thomas", last_name="Weber", email="weber@uni.de")

st1 = Student.objects.create(first_name="Max", last_name="Schmidt", email="max@uni.de")
st2 = Student.objects.create(first_name="Lisa", last_name="Fischer", email="lisa@uni.de")
st3 = Student.objects.create(first_name="Jonas", last_name="Becker", email="jonas@uni.de")

StudentCard.objects.create(student=st1, card_number="SC-2026-001")
StudentCard.objects.create(student=st2, card_number="SC-2026-002")
StudentCard.objects.create(student=st3, card_number="SC-2026-003")

d1 = CourseDescription.objects.create(text="Grundlagen der Datenbanken: relationales Modell, SQL, Normalisierung.")
d2 = CourseDescription.objects.create(text="Einfuehrung in die Programmierung mit Python.")
d3 = CourseDescription.objects.create(text="Webentwicklung mit Django: Modelle, Views, Templates.")

c1 = Course.objects.create(title="Datenbanken", professor=p1, description=d1, semester=s1)
c2 = Course.objects.create(title="Programmierung", professor=p2, description=d2, semester=s1)
c3 = Course.objects.create(title="Webentwicklung", professor=p1, description=d3, semester=s2)

c1.students.add(st1, st2, st3)
c2.students.add(st1, st3)
c3.students.add(st2)

print("Fertig!")   