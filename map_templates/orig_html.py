from datetime import date
def update_html(dir, number_of_charging_stations, number_of_vehicles, today=''):
    if not today:
        today = date.today().strftime("%Y/%m/%d")
    new_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
        <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
        <title>Stephanie Lojano - SGIL Fall 2020</title>
        <link rel="stylesheet" type="text/css" href="https://js.api.here.com/v3/3.1/mapsjs-ui.css" />
        <link rel="stylesheet" type="text/css" href="demo.css" />
        <link rel="stylesheet" type="text/css" href="styles.css" />
        <link rel="stylesheet" type="text/css" href="../template.css" />
        <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-core.js"></script>
        <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-service.js"></script>
        <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-ui.js"></script>
        <script type="text/javascript" src="https://js.api.here.com/v3/3.1/mapsjs-mapevents.js"></script>
    </head>
    <body id="markers-on-the-map">
        <div class="page-header">
            <h1>Stephanie Lojano - SGIL Research</h1>
            <h3>{today}</h3>
        </div>
            <p>This example shows {number_of_vehicles} vehicles connecting with {number_of_charging_stations} electric charging stations in Gowanus Brooklyn.</p>
        <div id="map">
        </div>
        <script type="text/javascript" src='demo.js'></script>
    </body>
    </html>
    '''
    with open(f'./{dir}/index.html', 'w') as html_file:
        html_file.write(new_html)

    css_template = '''
    #map {
        width: 95%;
        height: 900px;
        background: grey;
    }
    #panel {
        width: 100%;
        height: 400px;
    }
    '''
    with open(f'./{dir}/demo.css', 'w') as css_file:
        css_file.write(css_template)

