# [`folium_map.py`](../../folium_map.py)
`folium_map.py` is used for quick visualization of data using `folium`. `folium` is a Python wrapper for `leaflet.js` - an interactive maps module. Folium can render different style map types and can be saved as an HTML file for interaction. For the full documentation on the `folium` module, [visit their official documetation](https://python-visualization.github.io/folium/).

## `class folium_map`
### Attributes 
#### `folium_map.center_loc` : `Union[Tuple, List, Set, NumPy Array]`
- The center location of the map (WSG84 coordinates)- must be iteratible of size 2.
#### `folium_map._map` : `folium map`
- folium map object, instantiated with `self.center_loc`
### Methods
#### `folium_map.add_marker(marker_location, popup_text='', radius=7, edge_color='#ff14e4', fill_color='#e6a5de')`
**parameters:**
- **`marker_location`** : `Union[Tuple, List, Set, NumPy Array]`
    - location of marker to place on map (WSG84 coordinates) - must be iteratible of size 2. 
- **`popup_text`** *(optional, default=`''`)* : `str`
    - text to display when marker is clicked 
- **`radius`** *(optional, default=`7`)* : `int`
    - radius of marker, `folium` defined arbitrary units
- **`edge_color`** *(optional, default=`'#ff14e4'`)* : `str`
    - edge color of marker, must be hex color code. The default value is a neon pink color for visibility. For full range of hex color codes, look up hex color picker. 
- **`fill_color`** *(optional, default=`'#e6a5de'`)* : `str`
    - fill color of marker, must be hex color code. The default value is a pastel pink color for visibility. For full range of hex color codes, look up hex color picker. 
