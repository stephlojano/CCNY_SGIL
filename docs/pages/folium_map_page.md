# [`folium_map.py`](../../folium_map.py)
`folium_map.py` is used for quick visualization of data using `folium`. `folium` is a Python wrapper for `leaflet.js` - an interactive maps module. Folium can render different style map types and can be saved as an HTML file for interaction. For the full documentation on the `folium` module, [visit their official documetation](https://python-visualization.github.io/folium/).

## Contents
- **Requirements**
- **`class folium_map`**
    - [Attributes](###Attributes)
        - `self.center_loc`
    - Methods 
        - `self.__init__`
        - `self.add_marker`
        - `self.add_markers`
        - `self.add_polyline`
        - `self.add_polylines`
        - `self.save_map`
        - `self.display_map`
## Requirements 
You must have `Python 3.6` or above, and `folium` installed in order to use `folium_map.py`. You can install the latest version of `folium` with: 
```bash
pip install folium
```
If you on OSX or Linux without `pyenv`: 
```bash
pip3 install folium 
```


## `class folium_map`
### Attributes 
#### `folium_map.center_loc` : `Union[Tuple, List, Set, NumPy Array]`
- The center location of the map (WSG84 coordinates)- must be iterable of size 2.
#### `folium_map._map` : `folium map`
- folium map object, instantiated with `self.center_loc`
### Methods
#### `folium_map.__init__(center_location, init_zoom=13, tile_style="OpenStreetMap")`
**Parameters:**
- **`center_location`** : `Union[Tuple, List, Set, NumPy Array]`
    - location of marker to place on map (WSG84 coordinates) - must be iterable of size 2. 
- **`init_zoom`** *(optional, default=`13`)*: `int`
    - initial zoom of map. folium maps are interactive and zoom can be changed when displayed. 
- **`tile_style`** *(optional, default=`"OpenStreetMap"`)* : `str` 
    - tile style to use to display the map. Available free tiles are: 
        - `"OpenStreetMap"`
        - `"StamenTerrain"`
        - `"StamenToner"`
        - `"StamenWatercolor"`
        - `"CartoDBpositron"`
        - `"CartoDBdark_matter"`
    - see: https://python-visualization.github.io/folium/modules.html for more information on map files.

#### `folium_map.add_marker(marker_location, popup_text='', radius=7, edge_color='#ff14e4', fill_color='#e6a5de')`
Adds marker on the current folium map. 
**Parameters:**
- **`marker_location`** : `Union[Tuple, List, Set, NumPy Array]`
    - location of marker to place on map (WSG84 coordinates) - must be iterable of size 2. 
- **`popup_text`** *(optional, default=`''`)* : `str`
    - text to display when marker is clicked 
- **`radius`** *(optional, default=`7`)* : `int`
    - radius of marker, `folium` defined arbitrary units
- **`edge_color`** *(optional, default=`'#ff14e4'`)* : `str`
    - edge color of marker, must be hex color codeor color name as a string. The default value is a neon pink color for visibility. For full range of hex color codes, look up hex color picker. 
- **`fill_color`** *(optional, default=`'#e6a5de'`)* : `str`
    - fill color of marker, must be hex color code or color name as a string. The default value is a pastel pink color for visibility. For full range of hex color codes, look up hex color picker. 

#### `folium_map.add_markers(marker_locations, radius=7, edge_color='#ff14e4', fill_color='#e6a5de')`
Adds a collection of markers on the current folium map. 
**Parameters:**
 - **`marker_location`** : `Union[Tuple, List, Set, NumPy Array]`
    - Collection of locations (WSG84 coordinates) to add marker. Each coordinate of the collection must be an iterable of size 2.
- **`radius`** *(optional, default=`7`)* : `int`
    - radius of marker, `folium` defined arbitrary units
- **`edge_color`** *(optional, default=`'#ff14e4'`)* : `str`
    - edge color of marker, must be hex color code or color name as a string. The default value is a neon pink color for visibility. For full range of hex color codes, look up hex color picker. 
- **`fill_color`** *(optional, default=`'#e6a5de'`)* : `str`
    - fill color of marker, must be hex color code or color name as a string. The default value is a pastel pink color for visibility. For full range of hex color codes, look up hex color picker. 

#### `folium_map.add_polyline(start_pt, end_pt, color='blue', weight=1, opacity=1)` 
Connects two points with an undirected straight line (polyline). Folium does not provide support for directed polylines. 
**Parameters:**
- **`start_pt`** : `Union[Tuple, List, Set, NumPy Array]`
    - starting location of polyline (WSG84 coordinates) - must be iterable of size 2. 
- **`end_pt`** : `Union[Tuple, List, Set, NumPy Array]`
    - ending location of polyline (WSG84 coordinates) - must be iterable of size 2. 
- **`color`** *(optional, default=`'blue'`)* : `str`
    - fill color of polyline, must be hex color code or color name as a string. The default value is blue for visibility. For full range of hex color codes, look up hex color picker. 
- **`weight`** *(optional, default=`1`)* : `int`
    - weight of polyline. Increasing value means increasing weight.
- **`opacity`** *(optional, default=`1`)* : `float[0,1]`
    - opacity of polyline. Decreasing value increases transparency of polyline. 

#### `folium_map.add_polylines(points, color='blue', weight=1, opacity=1)` 
Connects an iterible of locations with an undirected straight line (polyline) on the current folium map. Folium does not provide support for directed polylines. The polyline is drawn in the same order passed into this method.
**Parameters:**
- **`marker_location`** : `Union[Tuple, List, Set, NumPy Array]`
    - Collection of WSG84 coordinates to connect. Each coordinate of the collection must be an iterable of size 2. The polyline is drawn in the same order in which this collection was passed in.
- **`color`** *(optional, default=`'blue'`)* : `str`
    - fill color of polyline, must be hex color code or color name as a string. The default value is blue for visibility. For full range of hex color codes, look up hex color picker. 
- **`weight`** *(optional, default=`1`)* : `int`
    - weight of polyline. Increasing value means increasing weight.
- **`opacity`** *(optional, default=`1`)* : `float[0,1]`
    - opacity of polyline. Decreasing value increases transparency of polyline. 

#### `folium_map.save_map(filename='')` 
Saves the current map as an HTML file. The target directory is always *`./saved_folium_maps`*
**Parameters:**
- **`filename`** *(optional, default=`''`)* : `str`
    - filename to save the current map. If no name is given, a random name will be generated using today's date. For example, `2021_01_27_dadfsadf.html`. The file will be located in *`./saved_folium_maps`*.

#### `folium_map.display_map()` 
Returns the current folium map object





