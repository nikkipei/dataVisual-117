import sys, csv
import pandas as pd

def htmldataVisual(path):
    csv_path = path
    hh = """
    <html>
      <head>
        <title>deck.gl + Mapbox HexagonLayer</title>
        <meta
          name="viewport"
          content="initial-scale=1,maximum-scale=1,user-scalable=no"/>

        <script src="https://unpkg.com/deck.gl@^6.2.0/deckgl.min.js"></script>
        <script src="https://api.tiles.mapbox.com/mapbox-gl-js/v0.50.0/mapbox-gl.js"></script>
        <link
          rel="stylesheet"
          type="text/css"
          href="https://api.tiles.mapbox.com/mapbox-gl-js/v0.50.0/mapbox-gl.css"/>
        <script src="https://d3js.org/d3.v5.min.js"></script>
       </head>
        <style>
            body {
              font-family: Helvetica, Arial, sans-serif;
              width: 100vw;
              height: 100vh;
              margin: 0;
            }
            #control-panel {
              position: absolute;
              background: #737373;
              top: 0;
              right: 0;
              margin: 12px;
              padding: 20px;
              font-size: 12px;
              line-height: 1.5;
              z-index: 1;
              border-radius: 8px;
              color: #f0f0f0;
            }
            label {
              display: inline-block;
              width: 90px;
              text-align: right;
              vertical-align: top;
              line-height: 20px;
              margin-right: 8px;
            }

      </style>
      <body>
        <div id="control-panel">
          <div>
            <label>Radius</label>
            <input
              id="radius"
              type="range"
              min="1000"
              max="20000"
              step="1000"
              value="1000"
            />
            <span id="radius-value"></span>
          </div>
          <div>
            <label>Coverage</label>
            <input
              id="coverage"
              type="range"
              min="0"
              max="1"
              step="0.1"
              value="1"
            />
            <span id="coverage-value"></span>
          </div>
          <div>
            <label>Upper Percentile</label>
            <input
              id="upperPercentile"
              type="range"
              min="90"
              max="100"
              step="1"
              value="100"
            />
            <span id="upperPercentile-value"></span>
          </div>
        </div>
      </body>
    <script >
        mapboxgl.accessToken =
      'pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoiY2pudzRtaWloMDAzcTN2bzN1aXdxZHB5bSJ9.2bkj3IiRC8wj3jLThvDGdA'


        const OPTIONS = ['radius', 'coverage', 'upperPercentile']
        const COLOR_RANGE = [
          [1, 152, 189],
          [73, 227, 206],
          [216, 254, 181],
          [254, 237, 177],
          [254, 173, 84],
          [209, 55, 78]
        ]
        const LIGHT_SETTINGS = {
          lightsPosition: [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
          ambientRatio: 0.4,
          diffuseRatio: 0.6,
          specularRatio: 0.2,
          lightsStrength: [0.8, 0.0, 0.8, 0.0],
          numberOfLights: 2
        }

        let hexagonLayer
        var longLat = 
        """
            
    hh2 = """;
        var featureCollection = [];

          for(var itemIndex in longLat) {
            // push new feature to the collection
            featureCollection.push({
              lat: parseFloat(longLat[itemIndex].slice(-1)),
              lng: parseFloat(longLat[itemIndex].slice(2,-1)),
              speed: parseFloat(longLat[itemIndex].slice(0,-3)),
              id: parseFloat(longLat[itemIndex].slice(1,-2))
              // "properties": 15
            });
          }
          const { MapboxLayer, HexagonLayer } = deck

        const map = new mapboxgl.Map({
          container: document.body,
          style: 'mapbox://styles/mapbox/dark-v9',
          center: [113.0527081, 28.17219876],
          zoom: 12,
          pitch: 40.5,
        })

        map.on('load', () => {
          hexagonLayer = new MapboxLayer({
            type: HexagonLayer,
            id: 'heatmap',
            data: featureCollection,
            radius: 5,
            coverage: 1,
            upperPercentile: 100,
            colorRange: COLOR_RANGE,
            getElevation:  d => [d.speed],
            elevationRange: [0, 20],
            elevationScale: 20,
            extruded: true,
            getPosition: d => [Number(d.lng), Number(d.lat)],
            transitions: {
                 getElevationValue: {
                    duration: 800
                 }
              },
            lightSettings: LIGHT_SETTINGS,
            opacity: 1
      })

      map.addLayer(hexagonLayer, 'waterway-label')
    })

    OPTIONS.forEach(key => {
      document.getElementById(key).oninput = evt => {
        const value = Number(evt.target.value)
        document.getElementById(key + '-value').innerHTML = value
        if (hexagonLayer) {
          hexagonLayer.setProps({ [key]: value })
        }
      }
    })
      </script>
    </html>
    """

    data = speedHex(csv_path)
    htmlText = hh+ str(data)+hh2
    return htmlText

def speedData(path):
    df = pd.read_csv(path, index_col=False, usecols=['frameNUM','carID','Lat','Lng'])
    p=df['carID'].max()
    # print(p)
    array = []
    for x in range(df['carID'].max()+1):
        try:
        # print(x)
            carid = df[df['carID']==x]
            if len(carid)>1:
                frame = (carid['frameNUM'].values[-1])-(carid['frameNUM'].values[0])
                speed = findSpeed(frame, carid['Lat'].values[0], carid['Lng'].values[0], carid['Lat'].values[-1], carid['Lng'].values[-1] )
                array.append([speed, carid['carID'].values[0],carid['Lng'].values[0], carid['Lat'].values[0] ])
            # print(array)
            else:
                array.append([0, carid['carID'].values[0],carid['Lng'].values[0], carid['Lat'].values[0] ])

        except:
            pass
    return array

def speedHex(path):
    df = pd.read_csv(path, index_col=False, usecols=['frameNUM','carID','Lat','Lng'])
    array = []
    for z in range(df['carID'].max()+1):
        try:
            carid = df[df['carID']==z]
            # seconds = 5 # ervery 5 secds
            # frameSecds = seconds*30 #150
            frameSecds = 50
            rang = (carid['frameNUM'].values[-1])-(carid['frameNUM'].values[0])
            numTime = math.floor(rang/frameSecds ) # ceiling 187/150
            #each car speed average in each 5 seconds
            for x in range(0, numTime):
                frame = carid[(carid['frameNUM']>= carid['frameNUM'].values[0]+(frameSecds*x)) & (carid['frameNUM']<= carid['frameNUM'].values[0]+(frameSecds*(x+1)))]
                time = (frame['frameNUM'].values[-1])-(frame['frameNUM'].values[0])
                speed = findSpeed(time, frame['Lat'].values[0], frame['Lng'].values[0], frame['Lat'].values[-1], frame['Lng'].values[-1] )
                array.append([speed, frame['carID'].values[0],frame['Lng'].values[0], frame['Lat'].values[0] ]) #car id
                # array.append([speed,frame['Lng'].values[0], frame['Lat'].values[0] ])

        except:
            pass

    return array
