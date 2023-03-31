# Bulk
A fitness app which lets users create workout plans, track eating, and set goals to improve their health. Gym routines can be created by specifying lift type and weight.
Runners with smart watches by companies like Garmin and Polar can upload their activity's .GPX file to view a map of their run, and see corresponding fitness data.

## Installation
This webserver requires Python 3.8 or later, with [Django](https://www.djangoproject.com/) and [gpxpy](https://github.com/tkrajina/gpxpy). All required packages can be installed using:
```
pip install -r requirements.txt
```

## Running the webserver
The Django development server can be run using the following command from the `bulk/` directory:
```
python manage.py runserver
```
