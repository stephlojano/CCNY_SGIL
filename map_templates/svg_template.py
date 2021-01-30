def create_svg_icon(location, label_text, fill_color, stroke_color="white"):

    svgstring = f'''
        var svgMarkup = '<svg width="24" height="24" ' +
            'xmlns="http://www.w3.org/2000/svg">' +
            '<rect stroke="white" fill="{fill_color}" x="1" y="1" width="22" ' +
            'height="22" /><text x="12" y="18" font-size="6pt" ' +
            'font-family="Arial" font-weight="bold" text-anchor="middle" ' +
            'fill="{stroke_color}">{label_text}</text></svg>';

        // Create an icon, an object holding the latitude and longitude, and a marker:
        var icon = new H.map.Icon(svgMarkup),
            coords = {{lat:{location[0]}, lng:{location[1]}}},
            marker = new H.map.Marker(coords, {{icon: icon}});

        // Add the marker to the map and center the map at the location of the marker:
        map.addObject(marker);
        map.setCenter(coords);
        '''

    return svgstring 