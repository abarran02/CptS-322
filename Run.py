import plotly.express as px
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from gpxpy.gpx import GPXTrackPoint # for typehinting
from gpxpy.gpx import GPX

class Run():
    def __init__(self, gpx: GPX, metric: bool = True):
        self.gpx = gpx
        self.geo_stats = {'distance':0, 'elevation_gain':0, 'elevation_loss':0}
        self.df = self.__convert_to_points(gpx)
        self.__generate_mapbox()
        self.metric = metric
        self.activity_stats = {'pace': '', 'calories': 0}
        self.__update_activity_stats()

    def __str__(self) -> str:
        merge = self.geo_stats | self.activity_stats
        return str(merge)

    def __update_geo_stats(self, previous: GPXTrackPoint, current: GPXTrackPoint) -> None:
        """Update geo_stats dictionary with additional distance and elevation between given GPXTrackPoints"""
        # calculate distance between points and add to total
        self.geo_stats['distance'] += haversine(previous.longitude, previous.latitude, 
                                        current.longitude, current.latitude)
        
        # if elevation is gained, add to gain
        if previous.elevation < current.elevation:
            self.geo_stats['elevation_gain'] += current.elevation - previous.elevation
        # otherwise add to loss
        elif previous.elevation > current.elevation:
            self.geo_stats['elevation_loss'] += previous.elevation - current.elevation

    def __convert_to_points(self, gpx: GPX) -> pd.DataFrame:
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

    def __generate_mapbox(self) -> None:
        # calculate automatic zoom
        zoom, center = zoom_center(
            lons=self.df['longitude'],
            lats=self.df['latitude']
        )

        # from https://plotly.com/python/lines-on-maps/
        self.mapbox = px.line_mapbox(self.df, lat='latitude', lon='longitude', hover_name='time', hover_data='distance',
                                color_discrete_sequence=["fuchsia"], zoom=(zoom-0.25), center=center)
        self.mapbox.update_layout(mapbox_style="open-street-map")
        self.mapbox.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    def __update_activity_stats(self) -> None:
        # calculate pace for total distance traveled
        dist = self.geo_stats['distance']
        if self.metric:
            unit = 'km'
            pace_seconds = self.gpx.get_duration() / dist
        else:
            unit = 'mi'
            miles = dist / 1.609
            pace_seconds = self.gpx.get_duration() / miles

        # convert total seconds to minutes and seconds mm:ss
        minutes = divmod(pace_seconds, 60)
        seconds = round(minutes[1])
        # lead seconds with one zero if single digit
        pace_string = f"{int(minutes[0])}:{seconds:02d}/{unit}"

        self.activity_stats['pace'] = pace_string

    def write_html(self, filename: str) -> None:
        # from https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
        self.mapbox.write_html(filename)

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
def zoom_center(lons: tuple, lats: tuple, width_to_height: float=2.0):
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
