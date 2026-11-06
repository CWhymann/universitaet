# Protokoll: Universitaetssystem mit Django

## Was ich gebaut habe

Ein Django-Projekt mit einer App namens "university". Die App modelliert
ein Universitaetssystem mit Studenten, Professoren, Kursen, Semestern
und Studentenausweisen. Die Beziehungen zwischen den Modellen entsprechen
exakt der Aufgabenstellung.

---

## Warum brauche ich Django?

Django ist ein Web-Framework. Es gibt mir:

- Ein ORM (Object-Relational-Mapping): Ich schreibe Python-Klassen,
  Django uebersetzt das automatisch in SQL und verwaltet die Datenbank.
- Ein Admin-Interface: Ich kann Daten ohne eigene HTML-Seiten verwalten.
- Eine URL-Routing-Struktur: Ich kann Views an URLs haeengen.

Ohne Django wuerde ich SQL-Tabellen manuell anlegen, HTML-Formulare
selbst bauen und die Daten per SQL-Abfragen lesen. Django macht
das alles fuer mich, solange ich die Regeln einhalte.

---

## Die Modelle – erklaert

### Student

    class Student(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)

Ich brauche ein Student-Modell, weil der Student die zentrale Person
im System ist. Er wird von anderen Modellen referenziert (Kurse,
Ausweis).

- CharField: Ein Textfeld mit fester Laenge. max_length ist Pflicht,
  weil Django damit das DB-Schema generiert (VARCHAR(100) in SQLite).
- EmailField: Wie CharField, aber Django validiert automatisch,
  dass das Format einer E-Mail entspricht (etwas@etwas.de).
- unique=True: Erzeugt ein UNIQUE-Constraint in der Datenbank.
  Ohne waere es moeglich, zwei Studenten mit derselben E-Mail
  anzulegen. Das soll nicht passieren.

**str** ist wichtig, weil Django es anzeigt, wenn das Objekt
als Text dargestellt wird – im Admin, in der Shell, in Templates.
Ohne **str** sahe ich "Student object (3)" statt "Max Schmidt".

---

### StudentCard – warum ein eigenes Modell?

    class StudentCard(models.Model):
        student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="card")
        card_number = models.CharField(max_length=50, unique=True)
        issued_at = models.DateField(auto_now_add=True)

Die Aufgabe sagt: "Jeder Student hat genau einen Studentenausweis."
Das ist eine 1:1-Beziehung.

Warum nicht einfach card_number = CharField() in Student?

- Weil der Ausweis ein eigenes Dokument ist mit eigener Information
  (Ausstellungsdatum, Nummer).
- Weil die Aufgabe explizit 1:1 verlangt.
- Weil es in der realen Welt so ist: Ein Student kann seinen
  Ausweis verlieren und einen neuen bekommen. Der Student bleibt,
  der Ausweis aendert sich.

OneToOneField funktioniert wie ForeignKey, aber mit UNIQUE-Constraint.
Das bedeutet: In der DB-Spalte student_id in der Tabelle
university_studentcard darf jeder Wert nur EINMAL vorkommen.
Ein Student kann also nur einen Ausweis haben.

on_delete=CASCADE: Wenn ich den Student loesche, wird der Ausweis
automatisch mitgeloescht. Das ist logisch – ein Ausweis ohne
Student existiert nicht.

related_name="card": Ermöglicht den Zugriff von der Parent-Seite.
student.card gibt den Ausweis zurueck. Ohne related_name wuerde
ich student.studentcard aufrufen muessen (Django-Default).

auto_now_add=True: Das Feld wird automatisch beim ersten Speichern
gesetzt. Ich muss es nie manuell befuellen.

---

### Professor

    class Professor(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)

Gleiche Logik wie Student. Die Aufgabe verlangt keine Department-
Struktur, also halte ich es minimal.

---

### Semester – warum ein eigenes Modell?

    class Semester(models.Model):
        name = models.CharField(max_length=50, unique=True)

Die Aufgabe sagt: "Ein Semester kann mehrere Kurse enthalten."
Das ist 1:N.

Warum nicht semester = CharField() in Course?

- Weil ich dann nicht leicht fragen koennte: "Gib mir alle Kurse
  im Sommersemester 2026." Ich wuerde alle Kurse mit
  semester="Sommersemester 2026" filtern muessen.
- Mit einem eigenen Modell + ForeignKey kann ich:
  Semester.objects.get(name="Sommersemester 2026").courses.all()
- Normalisierung: Wenn ich den Namen aendere, aendere ich eine
  Zeile, nicht alle Kurse.

unique=True: Es gibt nur EIN "Sommersemester 2026". Wenn ich
zwei anlege, waere das ein Fehler.

---

### CourseDescription – warum ein eigenes Modell?

    class CourseDescription(models.Model):
        text = models.TextField()

Die Aufgabe sagt: "Diese Beschreibung wird nur mit genau einem
Kurs verbunden." Das ist 1:1.

Warum nicht description = TextField() in Course?

- Weil die Aufgabe 1:1 verlangt.
- TextField() direkt in Course waere nur ein normales Feld,
  keine Beziehung.
- Mit OneToOneField in Course → CourseDescription ist es eine
  echte 1:1-Beziehung mit eigener Tabelle.

TextField statt CharField: Beschreibungen koennen lang sein.
CharField verlangt max_length, was hier unsinnig ist. TextField
hat keine Laengenbegrenzung.

---

### Course – das zentrale Modell

    class Course(models.Model):
        title = models.CharField(max_length=200)
        professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="courses")
        students = models.ManyToManyField(Student, related_name="courses", blank=True)
        description = models.OneToOneField(CourseDescription, on_delete=models.CASCADE, related_name="course")
        semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="courses")

Course ist das Modell, das alle Beziehungen zusammenfaellt:

1. professor = ForeignKey(Professor, ...)
   Die Aufgabe sagt: "Ein Professor kann mehrere Kurse unterrichten,
   aber jeder Kurs hat nur einen Professor." Das ist 1:N.
   Das ForeignKey steht auf der "Many"-Seite, also in Course.
   In der DB entsteht die Spalte professor_id in der Tabelle
   university_course. Jeder Kurs zeigt auf genau einen Professor.
   Ein Professor kann von vielen Kursen referenziert werden.

   on_delete=CASCADE: Professor weg → seine Kurse weg.
   related_name="courses": professor.courses.all() gibt alle
   seine Kurse zurueck.

2. students = ManyToManyField(Student, ...)
   Die Aufgabe sagt: "Ein Kurs kann von mehreren Studenten besucht
   werden und ein Student kann mehrere Kurse besuchen." Das ist M:N.
   Django erzeugt automatisch eine Junction-Table in der DB:
   university_course_students mit den Spalten course_id und
   student_id. Jede Zeile in dieser Tabelle ist eine Einschreibung.

   blank=True: Erlaubt, einen Kurs ohne Studenten anzulegen.
   Ohne blank=True wuerde Django bei der Form-Validierung
   meckern, wenn die M:N-Liste leer ist.

3. description = OneToOneField(CourseDescription, ...)
   1:1-Beziehung. Jeder Kurs hat genau eine Beschreibung.
   In der DB: Spalte description_id in university_course,
   mit UNIQUE-Constraint.

4. semester = ForeignKey(Semester, ...)
   1:N-Beziehung. Ein Semester enthaelt mehrere Kurse.
   In der DB: Spalte semester_id in university_course.

---

## on_delete – warum immer CASCADE?

on_delete sagt: "Was passiert mit den Kinder-Objekten, wenn das
Parent-Objekt geloescht wird?"

Ich habe bei allen CASCADE gewaehlt, weil in diesem System:

- Ein Kurs ohne Professor keinen Sinn ergibt.
- Ein Kurs ohne Semester keinen Sinn ergibt.
- Ein Kurs ohne Beschreibung keinen Sinn ergibt.
- Ein Ausweis ohne Student keinen Sinn ergibt.

Wenn ich PROTECT waehlen wuerde, koennte ich den Professor nie
loeschen, solange er Kurse hat. Das waere frustrierend.
Wenn ich SET_NULL waehle, brauche ich null=True und der Kurs
haette keinen Professor – auch unsinnig.

CASCADE ist hier die einfachste und logischste Wahl.

---

## admin.py – warum?

    from django.contrib import admin
    from .models import Student, StudentCard, Professor, Semester, CourseDescription, Course

admin.site.register(Student, inlines=[StudentCardInline])

admin.site.register() macht das Modell im Admin sichtbar.
Ohne diese Zeile erscheint das Modell NICHT in der Admin-
Uebersicht. Ich kann es nicht anlegen, nicht sehen, nicht loeschen.

StudentCardInline (TabularInline): Zeigt den Ausweis direkt
auf der Student-Edit-Seite an. Ich muss nicht erst in die
StudentCard-Liste gehen und dort den Student waehlen.
Ich sehe alles auf einer Seite.

CourseAdmin mit list_display: Bestimmt, welche Spalten in der
Uebersichtsliste erscheinen. Ohne list_display sahe ich nur
**str**. Mit list_display = ("title", "professor", "semester")
sehe ich drei Spalten auf einen Blick.

---

## views.py und urls.py – warum?

    def index(request):
        return render(request, "university/index.html", {
            "students": Student.objects.count(),
            ...
        })

Die View wird aufgerufen, wenn jemand http://127.0.0.1:8000/
oeffnet. Sie zaehlt die Objekte in der Datenbank und gibt die
Zahlen an das Template weiter. Das Template ersetzt {{ students }}
durch die Zahl.

urls.py verbindet die URL mit der View:

- path("", views.index) → leere URL = Root = /
- path("admin/", admin.site.urls) → /admin/ = Django-Admin

config/urls.py ist die "Haupt-URL-Datei". Sie entscheidet,
welche App welche URLs bekommt. include("university.urls")
sagt: "Alles, was nicht unter /admin/ ist, geh an die
university-App."

---

## Migrations – was passiert da?

    python manage.py makemigrations university

Django schaut sich models.py an und vergleicht es mit der
letzten Migration. Wenn sich was geaendert hat (neues Modell,
neues Feld, geaendertes Feld), erzeugt es eine neue Python-
Datei in university/migrations/. Diese Datei beschreibt in
Code, was die Datenbank tun soll (CREATE TABLE, ADD COLUMN,
etc.).

    python manage.py migrate

Fuehrt die Migrations-Dateien aus. Erst jetzt werden die
Tabellen in db.sqlite3 angelegt. Ohne migrate existieren
die Tabellen nicht, und jeder Datenbankzugriff schlaegt
mit "no such table" fehl.

---

## Zusammenfassung der Beziehungen

    Student ──1:1── StudentCard
    Professor ──1:N── Course
    Course ──M:N── Student
    Course ──1:1── CourseDescription
    Semester ──1:N── Course

Regeln:

- ForeignKey steht immer auf der "Many"-Seite.
- OneToOneField wie ForeignKey, aber mit UNIQUE.
- ManyToManyField erzeugt automatisch eine Junction-Table.
- on_delete entscheidet, was bei Loeschen passiert.
