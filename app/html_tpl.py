menu_items = '''
    <li><a href="javascript:void(0)" onclick="callHome()">Home</ae</li>
    <li><a href="javascript:void(0)" onclick="callGpio()">GPIO</a></li>
    <li><a href="javascript:void(0)" onclick="callGps()">GPS</a></li>
    <li><a href="javascript:void(0)" onclick="callThermistor()">Thermistor</a></li>
    <li><a href="javascript:void(0)" onclick="callProximity()">Proximity</a></li>
    '''

'''
============================================================

    Embedded CSS for performance. 
    Use {css_style} placeholder for string replacing the 
     css section in the html content

============================================================
'''
html = """ \
   <!DOCTYPE html>
    <html>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <head>
        <title>
         ESP32 Device Manager 
        </title>
        <link rel="icon" href="data:,"> 
        <link rel="stylesheet" type="text/css" href="css/styles.css">
        <script type="text/javascript" src="js/main.js"></script>
      </head>
      <body>
        <nav id="page-nav">
          <label for="hamburger">&#9776;</label>
          <input type="checkbox" id="hamburger"/>
          <label>ESP32 Device Manager</label>
          <ul>
          {menu_items}
          </ul>
        </nav>
        <div id="page-content" style="padding: 10px;">
            <center>
                <div id="app_view"></div>
            </center>
        </div>
      </body>
    </html>
   """

def getMainPage():
    return html.format(menu_items=menu_items)

