# Universitaetssystem

Django-basiertes Verwaltungssystem zur Modellierung von Studenten, Professoren, Kursen, Semestern und Studentenausweisen.

## Voraussetzungen

- Python 3.10 oder neuer
- Git

## Installation

Repository klonen:

```powershell
git clone https://github.com/CWhymann/universitaet.git
cd universitaet
```

Virtuelle Umgebung anlegen und aktivieren:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Abhängigkeiten installieren:

```powershell
pip install -r requirements.txt
```

Datenbank einrichten:

```powershell
python manage.py migrate
```

## Admin-Konto anlegen

```powershell
python manage.py createsuperuser
```

## Server starten

```powershell
python manage.py runserver
```

Danach im Browser öffnen:

- Startseite: http://127.0.0.1:8000/
- Admin-Oberfläche: http://127.0.0.1:8000/admin/ (Anmeldung mit dem Admin-Konto von oben)

## Projektstruktur

- `config/` – Projekteinstellungen und Haupt-URLs
- `university/` – App mit den Modellen `Student`, `StudentCard`, `Professor`, `Semester`, `Course` und `CourseDescription`
