from math import asin, cos, radians, sin, sqrt

import gpxpy
import numpy as np
import pandas as pd
import plotly.express as px
from django.conf import settings
from django.db import models
from gpxpy.gpx import GPX, GPXTrackPoint  # for typehinting


class Run(models.Model):
    title = models.CharField(max_length=64)
    
    # updated with __gpx_to_dataframe() and __update_geo_stats()
    distance = models.FloatField()
    time = models.DurationField()
    elevation_gain = models.IntegerField()

    # updated with __update_fitness_stats()
    pace = models.CharField(max_length=8)
    calories = models.IntegerField()

    # allow user GPX file upload to unique folder
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    gpx_upload = models.FileField(upload_to=f"uploads/{user}")

    def __str__(self) -> str:
        return self.title

    def generate_stats(self, weight: int = 0, metric: bool = True):
        """Generate Run distance, time, elevation gain, pace, and calories. Default is metric for distance in km and weight in kg."""
        gpx_stream = gpxpy.parse(self.gpx_upload)
        # convert given GPX to list of points for stats
        self.__gpx_to_dataframe(gpx_stream)
        # using geostats, calculate pace or calories
        self.__update_fitness_stats(weight, metric)

    def generate_mapbox_html(self):
        """Generate plotly mapbox HTML with lines for each GPX point with latitude and longitude"""
        gpx_stream = gpxpy.parse(self.gpx_upload)
        df = self.__gpx_to_dataframe(gpx_stream)
        # calculate automatic zoom
        zoom, center = zoom_center(
            lons=df['longitude'],
            lats=df['latitude']
        )

        # from https://plotly.com/python/lines-on-maps/
        mapbox = px.line_mapbox(df, lat='latitude', lon='longitude', hover_name='time', hover_data='distance',
                                color_discrete_sequence=["fuchsia"], zoom=(zoom-0.25), center=center)
        mapbox.update_layout(mapbox_style="open-street-map")
        mapbox.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        # from https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
        return mapbox.to_html()

    def __update_geo_stats(self, previous: GPXTrackPoint, current: GPXTrackPoint) -> None:
        """Add distance and elevation between given GPXTrackPoints"""
        # calculate distance between points and add to total
        self.distance += haversine(previous.longitude, previous.latitude, 
                                        current.longitude, current.latitude)

        # if elevation is gained, add to gain
        if previous.elevation < current.elevation:
            self.elevation_gain += current.elevation - previous.elevation

    def __gpx_to_dataframe(self, gpx: GPX) -> pd.DataFrame:
        """Convert GPX points to Pandas dataframe"""
        # from https://www.gpxz.io/blog/gpx-file-to-pandas
        points = []
        previous = gpx.tracks[0].segments[0].points[0]
        # Convert to a dataframe one point at a time.
        for segment in gpx.tracks[0].segments:
            for current in segment.points:
                self.__update_geo_stats(previous, current)

                points.append({
                    'time': current.time,
                    'latitude': current.latitude,
                    'longitude': current.longitude,
                    'elevation': current.elevation,
                    'distance': round(self.geo_stats['distance'], 2)
                })

                previous = current

        # convert list to dataframe
        return pd.DataFrame.from_records(points)

    def __update_fitness_stats(self, weight: int = 0, metric: bool = True) -> None:
        """Calculate pace for total distance and calories burned for total time"""
        distance = self.distance
        seconds = self.time

        # calculate pace to string mm:ss/km and calories burned
        self.pace = calculate_running_pace(seconds, distance, metric)
        self.calories = calculate_calories_burned(seconds, weight, metric)

# from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6378.1 # Radius of earth in kilometers
    return c * r

# from https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
def zoom_center(lons: tuple, lats: tuple, width_to_height: float=2.0) -> tuple:
    """Finds optimal zoom and centering for a plotly mapbox.
    
    Parameters
    --------
    lons: tuple, optional, longitude component of each location
    lats: tuple, optional, latitude component of each location
    width_to_height: float, expected ratio of final graph's with to height,
        used to select the constrained axis.
    
    Returns
    --------
    zoom: float, from 1 to 20
    center: dict, gps position with 'lon' and 'lat' keys
    """
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    margin = 1.2
    height = (maxlat - minlat) * margin * width_to_height
    width = (maxlon - minlon) * margin
    lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
    lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)
    
    return zoom, center

def calculate_running_pace(seconds: int, distance: float, metric: bool = True) -> str:
    if metric:
        unit = 'km'
        pace_seconds = seconds / distance
    else:
        unit = 'mi'
        miles = distance / 1.609
        pace_seconds = seconds / miles

    # convert total seconds to minutes and seconds mm:ss
    minutes = divmod(pace_seconds, 60)
    seconds = round(minutes[1])
    # lead seconds with one zero if single digit
    return f"{int(minutes[0])}:{seconds:02d}/{unit}"

def calculate_calories_burned(seconds: int, weight: int, metric: bool = True) -> float:
    """Calculate activity calories burned using the equation = MET * weight (kg) * time (hrs)"""
    # https://marathonhandbook.com/how-many-calories-burned-running-calculator/#met-formula
    if not metric:
        # convert kilograms to pounds
        weight /= 2.205
    return 10 * weight * (seconds / 3600)
