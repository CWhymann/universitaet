# Universitaetssystem

Django-basiertes Verwaltungssystem.

## Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Admin

Die Admin-Oberfläche erreichst du unter:

```
http://127.0.0.1:8000/admin/
```