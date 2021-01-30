# Documentation for SmartGrid Interdependecy Labs at the City College of New York 

These pages will be document the usage of all functions written in the Fall 2020 semester at the City College of New York. Some of these functions may not be optimized and may need to be changed. Please contact slojano000@citymail.cuny.edu with any questions. 

## Dependencies 
In order to use the `SGIL` module, you must first install: 
- Python 3.6 and above 
- folium:
    - ```pip install folium``` or ```pip3 install folium``` 
- `flexible_polyline`:
    - Clone this repository and in your CLI, type:
        - `cd ./flexible_polyline/`
        - `python setup.py install`

## Page Navigation
- #### [folium_map.py](./pages/folium_map_page.md)
    - used to create quick maps with `folium` - a Python wrapper for `leaflet` 
- #### geoutil.py 
    - utility functions for geographical calculations
- #### gowanus_map.py 
    - a Python `dict` of points in the Gowanus, Brooklyn area 
        - key=`point number`: value = `location` 
- #### here_maps_visualizer.py 
    - uses `here API` map tiles to draw/create a map with boiler plate html, CSS, and javascript
- #### hereAPI.py 
    - used to interact with `here REST API` 
- #### SGIL_solver.py 
    - used to solve the routing problem - used in conjunction with `hereAPI.py` 

