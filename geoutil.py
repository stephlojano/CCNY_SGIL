import flexpolyline as fp
import math

def decode_polyline(polyline_str):
    return fp.decode(polyline_str)

def encode_to_polyline(coordinates):
    return fp.encode(coordinates)

def get_distance(location1, location2):
    '''Returns the distance between two WSG84 points using Haversine Formula'''
    radius = 6.378137e6 # radius of the earth

    lat1, lon1 = math.radians(location1[0]), math.radians(location1[1])
    lat2, lon2 = math.radians(location2[0]), math.radians(location2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    prod = math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    a = math.sin(dlat / 2)**2 + prod    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c # distance in meters

    return distance 

def within_proximity(location1, location2, radius=25):
    '''Checks if two WSG84 points are within or equal to radius meters of each other'''
    return (get_distance(location1, location2) <= radius)

if __name__ == '__main__':
    point1 = (40.678135, -73.990912)
    point2 = (40.678703, -73.990411)
    print(get_distance((40.678135, -73.990912), (40.678703, -73.990411)))
    print(within_proximity(point1, point2))
