# Bulk

This project was created by Alec Barran, Matthew Wong, Elijah Lin, Tyson Diep, and Harry Pulivarthy for the Spring 2023 section of CptS 322 at Washington State University. The group assignment focused on modeling the software design process, followed by efficient implementation using the documentation produced throughout the semester.

Bulk fitness app which lets users set calorie goals and track gym workouts, runs, swims, and meals. Runners with smart watches by companies like Garmin can upload their .GPX files to view their run's map and data. Users can follow each other and see their friends' activities.

## Installation

This [Django](https://www.djangoproject.com/) webserver requires Python 3.8 or later. All required packages can be installed using:

```Bash
pip install -r requirements.txt
```

The most notable libraries in use are [gpxpy](https://github.com/tkrajina/gpxpy) and [plotly](https://github.com/plotly/plotly.py), used for parsing .GPX files and generating a map of the location points.

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
