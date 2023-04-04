
# https://pypi.org/project/gpxpy/

import gpxpy
import plotly.express as px
import pandas as pd
import numpy as np

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
for segment in gpx.tracks[0].segments:
    for p in segment.points:
        points.append({
            'time': p.time,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'elevation': p.elevation,
        })
df = pd.DataFrame.from_records(points)

# from https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
zoom, center = zoom_center(
    lons=df['longitude'],
    lats=df['latitude']
)

# from https://plotly.com/python/lines-on-maps/
fig = px.line_mapbox(df, lat='latitude', lon='longitude', hover_name='time',
                        color_discrete_sequence=["fuchsia"], zoom=(zoom-0.25), center=center)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# from https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
fig.write_html("sample.html")
