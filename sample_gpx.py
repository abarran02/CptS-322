# https://pypi.org/project/gpxpy/
import gpxpy
from Run import Run

if __name__ == "__main__":
    # Load gpx.
    gpx_path = 'sample.gpx'
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    run = Run(gpx, metric=True)
    # print gpx stats
    print(run.activity_stats)
    print(run.geo_stats)

    print(run)
