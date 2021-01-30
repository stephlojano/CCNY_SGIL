boiler_plate = '''
/**
 * Adds the polylines
 *
 * @param  {H.Map} map      A HERE Map instance within the application
 */

function addPolygonToMap(map, values) {
    var lineString = new H.geo.LineString(
      values,
      'values lat lng alt'
    );
    map.addObject(
      new H.map.Polygon(lineString, {
        style: {
          fillColor: '#ff0000',
          strokeColor: '#ff0000',
          lineWidth: 3
        }
      })
    );
  }
function addMarker(map, location, color){
    var marker = new H.map.Circle(location, 13,
        {
            style:
            {
                fillColor: color
            }
        });
    map.addObject(marker);
}
function addPolylineToMap(map, polyline, start, end, width, color) {
    // var lineString = new H.geo.LineString.fromFlexiblePolyline("BGgy-ytCt42jtErFiOzFsO_T0yBgU4N4SwMwHgFoQoLwR8L4X8QsOsJ0oB8a8QoL2KsH");
    var lineString = new H.geo.LineString.fromFlexiblePolyline(polyline);
    // var Circle = new H.map.Circle({lat:40.680594, lng:-73.989123}, 50,
    //     {
    //         style:
    //         {
    //             fillColor: 'rgba(252, 71, 255, 0.7)'
    //         }
    //     });
    var startCircle = new H.map.Circle(start, 25,
        {
            style:
            {
                fillColor: 'rgba(252, 71, 255, 0.7)'
            }
        });
    var endCircle = new H.map.Circle(end, 50,
        {
            style:
            {
                fillColor: 'rgba(0, 255, 51, 0.7)'
            }
        });

    // var coordinates = [{lat:40.680594, lng:-73.989123}, {lat:40.676281, lng:-73.986730}, {lat:40.666349, lng:-73.992390}];
    // var i; 
    // for (i = 0; i < coordinates.length; i++){
    //     lineString.pushPoint(coordinates[i]);
    // }
    map.addObject(new H.map.Polyline(
      lineString, { style: { lineWidth: width, strokeColor: color}}
    ));
    map.addObject(startCircle);
    map.addObject(endCircle);
  }
  
/**
 * Boilerplate code from Here API:
 */

//Step 1: initialize communication with the platform
var platform = new H.service.Platform({
'apikey': '{Uu1shEwIITRCL0aNwAoFDt4Cxn7JFz1DuaezTryp7P4}'
});
var defaultLayers = platform.createDefaultLayers();

//Step 2: initialize a map - this map is centered over Gowanus, NYC
var map = new H.Map(document.getElementById('map'),
    defaultLayers.vector.normal.map,{
    center: {lat:40.675308, lng:-73.991096},
    zoom: 15,
    pixelRatio: window.devicePixelRatio || 1
});

// add a resize listener to ensure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

// Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI components from Here API
var ui = H.ui.UI.createDefault(map, defaultLayers);
'''