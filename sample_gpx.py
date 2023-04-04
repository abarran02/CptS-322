
# https://pypi.org/project/gpxpy/

import gpxpy
import plotly.express as px
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

# from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
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

# from https://www.gpxz.io/blog/gpx-file-to-pandas
# Load gpx.
gpx_path = 'sample.gpx'
with open(gpx_path) as f:
    gpx = gpxpy.parse(f)

# Convert to a dataframe one point at a time.
points = []
total_distance = 0
previous_point = gpx.tracks[0].segments[0].points[0]
for segment in gpx.tracks[0].segments:
    for p in segment.points:
        total_distance += haversine(previous_point.longitude, previous_point.latitude, 
                                        p.longitude, p.latitude)
        points.append({
            'time': p.time,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'elevation': p.elevation,
            'distance': round(total_distance, 2)
        })

        previous_point = p
df = pd.DataFrame.from_records(points)

zoom, center = zoom_center(
    lons=df['longitude'],
    lats=df['latitude']
)

# from https://plotly.com/python/lines-on-maps/
fig = px.line_mapbox(df, lat='latitude', lon='longitude', hover_name='time', hover_data='distance',
                        color_discrete_sequence=["fuchsia"], zoom=(zoom-0.25), center=center)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# from https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
fig.write_html("sample.html")

if __name__ == "__main__":
    # calculate the total distance traveled and pace
    metric = True
    if metric:
        print(f"{round(total_distance, 2)} km")
        pace = gpx.get_duration() / total_distance

        minutes = divmod(pace, 60)
        seconds = round(minutes[1])
        # lead seconds with one zero if single digit
        print(f"{int(minutes[0])}:{seconds:02d}/km")
    else:
        miles = total_distance / 1.609
        print(f"{round(miles, 2)} mi")
        pace = gpx.get_duration() / miles

        minutes = divmod(pace, 60)
        seconds = round(minutes[1])
        print(f"{int(minutes[0])}:{seconds:02d}/mi")
