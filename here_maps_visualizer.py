from .map_templates.orig_js import boiler_plate
from .map_templates.orig_html import update_html
from .map_templates.utils import generate_random_name
from .map_templates.svg_template import create_svg_icon
import os 
from random import randint

class html_map:
    def __init__(self, map_nodes, charging_stations, vehicle_locations, map_name='', solution=None, map_node_color='rgba(78, 66, 245, 0.9)'):
        self.map_nodes = map_nodes # this is the underlying map - i.e. all of the intersection locations 
        self.map_node_color = map_node_color # (r,g,b,a) where a is alpha value (transparency)
        self.solution = solution

        self.map_name = map_name

        self.charging_stations = {}
        for idx, loc in enumerate(charging_stations):
            self.charging_stations[idx] = loc

        self.vehicle_locations = {}
        for idx, loc in enumerate(vehicle_locations):
            self.vehicle_locations[idx] = loc

        if not self.map_name:
            self.map_name = generate_random_name()
        
        if not os.path.isdir(self.map_name):
            os.mkdir(self.map_name)
            
    def draw_map(self, draw_nodes=False, draw_vehicles=False, draw_charging_stations=False, node_labels=False, vehicle_labels=False, station_labels=False, draw_roadblocks=False):
        with open(f"./{self.map_name}/demo.js", 'w') as js_file:
            js_file.write(boiler_plate + '\n')
        
        update_html(self.map_name,len(self.charging_stations), len(self.vehicle_locations))

        if draw_nodes:
            with open(f"./{self.map_name}/demo.js", 'a') as js_file:
                for key, value in self.map_nodes.items():
                    js_file.write(f"var nodes{key} = {{lat:{value[0]}, lng:{value[1]}}};\n")
                    js_file.write(f"addMarker(map, nodes{key}, '{self.map_node_color}');\n\n")
                    if node_labels:
                        icon = create_svg_icon(value, 'N' + str(key), fill_color="black")
                        js_file.write(icon)

        if draw_vehicles:
            pass 

        if draw_charging_stations:
            pass 
            
        if draw_roadblocks:
            pass

    def draw_route(self, vehicle_number, polylines, solution=None, color=None):
        assert(self.solution != None or solution != None), "No route to draw. Define solution dict with .define_solution or as a parameter of this function."
        
        if self.solution:
            station = self.solution[vehicle_number]
        if solution:
            station = solution[vehicle_number]
        
        polyline = polylines[vehicle_number][station]

        if color:
            r, g, b = color 
        else:
            r, g, b = 255, 0, 0

        cnt = randint(0, 1000)
        with open(f"./{self.map_name}/demo.js", 'a') as js_file:
            js_file.write(f"var polyline{cnt} = \"{polyline}\";\n")
            js_file.write(f"var origin{cnt} = {{lat:{self.vehicle_locations[vehicle_number][0]}, lng:{self.vehicle_locations[vehicle_number][1]}}};\n")
            js_file.write(f"var dest{cnt} = {{lat:{self.charging_stations[station][0]}, lng:{self.charging_stations[station][1]}}};\n")
            js_file.write(f"addPolylineToMap(map, polyline{cnt}, origin{cnt}, dest{cnt},{3}, 'rgba({r}, {g}, {b}, 0.9)');\n")

    def define_solution(self, solution):
        self.solution = solution

    def draw_route_without_hist(self, vehicle_number, station, polyline):
        r, g, b = 255, 0, 0
        cnt = randint(0, 1000)
        with open(f"./{self.map_name}/demo.js", 'a') as js_file:
            js_file.write(f"var polyline{cnt} = \"{polyline}\";\n")
            js_file.write(f"var origin{cnt} = {{lat:{self.vehicle_locations[vehicle_number][0]}, lng:{self.vehicle_locations[vehicle_number][1]}}};\n")
            js_file.write(f"var dest{cnt} = {{lat:{self.charging_stations[station][0]}, lng:{self.charging_stations[station][1]}}};\n")
            js_file.write(f"addPolylineToMap(map, polyline{cnt}, origin{cnt}, dest{cnt},{3}, 'rgba({r}, {g}, {b}, 0.9)');\n")


        