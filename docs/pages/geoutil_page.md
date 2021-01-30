# [`geoutil.py`](../../geoutil.py)
`geoutil.py` contains various utility functions for geographical visualizations and calculations. 

## Contents 
- **Requirements**
- **Geographical Utility Functions**
    - `geoutil.decode_polyline`
    - `geoutil.encode_to_polyline` 
    - `geoutil.get_distance` 
    - `geoutil.within_proximity`
- **Information on Polylines**
---

## Requirements 
You must have `Python 3.6` or above, and `flexible_polyline` installed in order to run some of the functions included here. To set up `flexible_polyline`, navagate to the beginning of this directory and use the commands: 
```bash
cd ./flexible_polyline
python setup.py install # or python3 if you are on OSX/Linux
```
---
## Geographical Utility Functions 
#### `geoutil.decode_polyline(polyline_str)`
**Parameters:**
- `polyline_str` : `str` 
    - `Here API` specific flexible polyline as a string. For more information on how `Here API`, visit the last section of this page. 

**Returns:**
- This function returns a `List` of WSG84 coordinates that the flexible polyline originally represented. 
---
#### `geoutil.encode_to_polyline(coordinates)`
**Parameters:**
- `coordinates` : `Union[List, Tuple]` 
    - encodes an iterable of WSG84 coordinates to `Here API` flexible polyline format. The polyline is formed in the order of the input coordinates. 

**Returns:**
- Returns an encoded `Here API` flexible polyline string. 
---

#### `geoutil.get_distance(location1, location2)`
Finds the absolute distance between two WSG84 coordinates in *meters*.
**Parameters:**
- `location1` : `Union[List, Tuple, Set]`  
    - WSG84 coordinates representing the first location. 
- `location2` : `Union[List, Tuple, Set]`  
    - WSG84 coordinates representing the second location. 

**Returns:**
- The distance between `location1` and `location2` in *meters*. 
---
#### `geoutil.within_proximity(location1, location2, radius=25)`
Checks whether two WSG84 coordinates are within `radius` distance of each other. 

**Parameters:**
- `location1` : `Union[List, Tuple, Set]`  
    - WSG84 coordinates representing the first location. 
- `location2` : `Union[List, Tuple, Set]`  
    - WSG84 coordinates representing the second location. 
- `radius` *(optional, default=25)* : `float`
    - threshold distance (in *meters*) to check for 

**Returns:**
- Returns a `boolean` representing whether the two WSG84 locations are within `radius` distance of each other. 

---


## Information on Polylines 
`Here API` specific flexible polylines are a variant of the [*Encoded Polyline Algorithm Format*](https://developers.google.com/maps/documentation/utilities/polylinealgorithm). This variant provides several advantages over the original implementation: 
- Output string is composed by only URL-safe characters, i.e. may be used without URL encoding as query parameters.
- Floating point precision is configurable: This allows to represent coordinates with precision up to microns (5 decimal places allow meter precision only).
- It allows to encode a 3rd dimension with a given precision, which may be a level, altitude, elevation or some other custom value.

For more information on how this encoding works, visit: https://github.com/heremaps/flexible-polyline 