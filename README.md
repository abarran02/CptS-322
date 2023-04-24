# Bulk

A fitness app which lets users set goals and track gym routines, runs, and meals to improve their health. Runners with smart watches by companies like Garmin and Polar can upload their activity's .GPX file to view a map of their run, and see fitness data.

## Installation

This [Django](https://www.djangoproject.com/) webserver requires Python 3.8 or later. All required packages can be installed using:

```Bash
pip install -r requirements.txt
```

## Running the webserver

Before running the Django development server, you must generate the SQLite database by running the following commands from the `bulk/` directory:

```Bash
python manage.py makemigrations accounts posts
python manage.py migrate
```

Then, the server can be run using:

```Bash
python manage.py runserver
```

If you need to regenerate the SQLite database, you must delete all `migrations/` and `__pycache__/` folders, then run `makemigrations` and `migrate` again.
