# Setup Guide

BORDLE runs on a few different libraries.

To run BORDLE locally you will need these things installed:
- python3
- flask
- geopandas
- numpy
- shapely

To run, download the directory along with [countries.geojson](https://datahub.io/core/geo-countries) if you are downloading from GitHub. If you are downloading from GitHub, move countries.geojson into the bordle directory (AKA the directory this file should be in). If you didn't dowload this from GitHub, you probably allready have the file and will not need to do this. 

To run, go into a terminal and enter the directory with the code. Run the command `export FLASK_APP=server` if on Bash and `set FLASK_APP=server` if on CMD. Then run `flask run`. Copy the URL it says it is running on into a browser. At this point you should see the site properly functioning. Please do not use Internet Explorer. To end the program, use `^C` (control C).
