import folium as flm
import os 

class folium_map:
    def __init__(self, center_location, init_zoom=13, tile_style="OpenStreetMap"):
        '''Initalizes a class that that uses folium maps'''
        self.center_loc = center_location

        # initialize the map object from folium as a protected member of this class 
        self._map = flm.Map(location=self.center_loc, zoom_start=init_zoom, tiles=tile_style)
        
    def add_marker(self, marker_location, popup_text='', radius=7, edge_color='#ff14e4', fill_color='#e6a5de'):
        '''adds a marker at a specific location of the map'''
        marker = flm.CircleMarker(location=marker_location, popup=popup_text, radius=radius, color=edge_color,
                                fill=True, fill_color=fill_color)
        marker.add_to(self._map)

    def add_markers(self, marker_locations, radius=7, edge_color='#ff14e4', fill_color='#e6a5de'):
        ''' '''
        for i, loc in enumerate(marker_locations):
            text = f'{i}'
            self.add_marker(loc, popup_text=text, radius=radius, edge_color=edge_color, fill_color=fill_color)

    def add_polyline(self, start_pt, end_pt, color='blue', weight=1, opacity=1):
        '''adds a line from a starting point to ending point. Note: this line is undirected. 
        Directed lines are currently unsupported by folium''' 
        line = flm.PolyLine([start_pt, end_pt], color=color, weight=weight, opacity=opacity)
        line.add_to(self._map)

    def add_polylines(self, points, color='blue', weight=1, opacity=1):
        ''' '''
        for i in range(len(points)-1):
            self.add_polyline(points[i], points[i+1], color=color, weight=weight, opacity=opacity)
        self.add_polyline(points[-1], points[0],color=color, weight=weight, opacity=opacity)
    
    def save_map(self, filename=''):
        '''saves the map to a html file. If no name is given, then a name will be randomly generated with today's date'''
        if not os.path.isdir('./saved_folium_maps'):
            os.mkdir('saved_folium_maps')
            
        if not filename:
            from random import choice 
            from datetime import date
            filename = ''.join(choice([chr(ascii) for ascii in range(97,123)]) for i in range(7))
            filename = date.today().strftime("%Y-%m-%d") + '_' + filename

        if filename[-5:] != ".html":
            filename += '.html'

        filename = os.path.join('saved_folium_maps', filename)
        self._map.save(filename)
        print(f'Map saved as {filename}')

    def display_map(self):
        return self._map


    