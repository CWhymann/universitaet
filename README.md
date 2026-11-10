# University System

Django-based administration system for modeling students, professors, courses, semesters, and student ID cards.

## Prerequisites

- Python 3.10 or newer
- Git

## Installation

Clone the repository:

```powershell
git clone https://github.com/CWhymann/universitaet.git
cd universitaet
```

Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Set up the database:

```powershell
python manage.py migrate
```

## Create an Admin Account

```powershell
python manage.py createsuperuser
```

## Start the Development Server

```powershell
python manage.py runserver
```

Then open the following URLs in your browser:

- Home page: http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/ (log in using the admin account created above)

## Project Structure

- `config/` – Project settings and main URL configuration
- `university/` – Django application containing the models `Student`, `StudentCard`, `Professor`, `Semester`, `Course`, and `CourseDescription`