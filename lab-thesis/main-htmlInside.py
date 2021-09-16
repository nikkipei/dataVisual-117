from editor import (
    Editor,
    TOOL_ADD_ARC,
    TOOL_ADD_REGION,
    TOOL_REMOVE_ARC,
    TOOL_REMOVE_REGION,
    loadCSV,
    loadVsCSV,
    saveCSV,
)
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from player import Player
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

os.chdir(os.path.dirname(sys.argv[0]))

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app = QApplication(sys.argv)

app.setStyle(QStyleFactory.create("fusion"))
palette = QPalette()
palette.setColor(QPalette.Window, QColor(19, 19, 19))
palette.setColor(QPalette.WindowText, QColor(194, 194, 194))
palette.setColor(QPalette.Base, QColor(100, 100, 100))
palette.setColor(QPalette.Background, QColor(19, 19, 19))
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(100, 100, 100))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.white)
app.setPalette(palette)

window = QMainWindow()
uic.loadUi("../ui/MainWindow.ui", window)

video_parent = window.findChild(QWidget, "videoParent")
video_next_btn = window.findChild(QPushButton, "videoNextBtn")
video_pause_btn = window.findChild(QPushButton, "videoPauseBtn")
video_play_btn = window.findChild(QPushButton, "videoPlayBtn")
video_previous_btn = window.findChild(QPushButton, "videoPreviousBtn")
video_stop_btn = window.findChild(QPushButton, "videoStopBtn")

action_open_csv = window.findChild(QAction, "actionOpen_CSV")
action_open_video = window.findChild(QAction, "actionOpen_Video")
action_save_csv = window.findChild(QAction, "actionSave_CSV")
action_save_csv_as = window.findChild(QAction, "actionSave_CSV_As")
action_quit = window.findChild(QAction, "actionQuit")
action_add_arc = window.findChild(QAction, "actionAdd_Arc")
action_remove_arc = window.findChild(QAction, "actionRemove_Arc")
action_add_region = window.findChild(QAction, "actionAdd_Region")
action_remove_region = window.findChild(QAction, "actionRemove_Region")
action_zoom_in = window.findChild(QAction, "actionZoom_In")
action_zoom_out = window.findChild(QAction, "actionZoom_Out")

frames_slider = window.findChild(QSlider, "framesSlider")
frames_count_label = window.findChild(QLabel, "framesCountLabel")
frame_spin_box = window.findChild(QSpinBox, "frameSpinBox")

car_id_edit = window.findChild(QLineEdit, "carIDEdit")
car_info_save_btn = window.findChild(QPushButton, "carInfoSaveBtn")

neighbor_frames = window.findChild(QListWidget, "neighborFrames")

player = Player(neighbor_frames)
video_parent.layout().addWidget(player, 0, 0)

video_next_btn.clicked.connect(lambda: player.nextFrame())
video_pause_btn.clicked.connect(lambda: player.pause())
video_play_btn.clicked.connect(lambda: player.play())
video_previous_btn.clicked.connect(lambda: player.prevFrame())
video_stop_btn.clicked.connect(lambda: player.stop())

editor = Editor(player, car_id_edit, car_info_save_btn, video_parent)
video_parent.layout().addWidget(editor, 0, 0)
editor.raise_()

csv_path = None


def onOpenCSV():
    global csv_path
    path, _ = QFileDialog.getOpenFileName(
        window,
        "Open CSV",
        filter="All files (*.*);;CSV (*.csv)",
    )
    if path:
        csv_path = path
        print(f"Loading CSV: {path}")
        print(path)
        data = loadCSV(csv_path)
        # loadVsCSV(csv_path)        
        editor.setData(data)
        hh = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Display buildings in 3D</title>
        <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.4.1/mapbox-gl.css" rel="stylesheet">
        <script src="https://api.mapbox.com/mapbox-gl-js/v2.4.1/mapbox-gl.js"></script>
        <script src='csv2geojson.js'></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>

        <style>
        body { margin: 0; padding: 0; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        </style>
        </head>
        <body>
        <div id="map"></div>
        <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuc3dpY2siLCJhIjoiY2l1dTUzcmgxMDJ0djJ0b2VhY2sxNXBiMyJ9.25Qs4HNEkHubd4_Awbd8Og';
        var map = new mapboxgl.Map({
            container: 'map', // container id
            style: 'mapbox://styles/mapbox/streets-v8', //stylesheet location
            center: [ 113.048778519374, 28.1721735387714], // starting position
            zoom: 10 // starting zoom
            // center: [ -89.89709901792442, 41.29146740952274], // starting position
            // zoom: 3 // starting zoom
        });

        $(document).ready(function() {
            $.ajax({
                type: "GET",
                url: ,
                // url: './DJI_0002stab_latlng.csv',

                dataType: "text",
                success: function(csvData) {makeGeoJSON(csvData);}
             });
        });

        function makeGeoJSON(csvData) {
            csv2geojson.csv2geojson(csvData, {
                latfield: 'Lat',
                lonfield: 'Lng',
                // latfield: 'latitude',
                // lonfield: 'longitude',
                delimiter: ','
            }, function(err, data) {
                map.on('load', function () {
                    map.addSource('airports', {
                    type: 'geojson',
                    data: data
                  });
                    map.addLayer(
          {
            id: 'airports-heat',
            type: 'heatmap',
            source: 'airports',
            maxzoom: 15,
            paint: {
              // increase weight as diameter breast height increases
              'heatmap-weight': {
                property: 'carID',
                type: 'exponential',
                stops: [
                  [1, 0],
                  [62, 1]
                ]
              },
              // increase intensity as zoom level increases
              'heatmap-intensity': {
                stops: [
                  [11, 1],
                  [15, 3]
                ]
              },
              // assign color values be applied to points depending on their density
              'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0,
                'rgba(236,222,239,0)',
                0.2,
                'rgb(208,209,230)',
                0.4,
                'rgb(166,189,219)',
                0.6,
                'rgb(103,169,207)',
                0.8,
                'rgb(28,144,153)'
              ],
              // increase radius as zoom increases
              'heatmap-radius': {
                stops: [
                  [11, 15],
                  [15, 20]
                ]
              },
              // decrease opacity to transition into the circle layer
              'heatmap-opacity': {
                default: 1,
                stops: [
                  [14, 1],
                  [15, 0]
                ]
              }
            }
          },
          'waterway-label'
        );

        map.addLayer(
          {
            id: 'airports-point',
            type: 'circle',
            source: 'airports',
            minzoom: 14,
            paint: {
              // increase the radius of the circle as the zoom level and dbh value increases
              'circle-radius': {
                property: 'carID',
                type: 'exponential',
                stops: [
                  [{ zoom: 15, value: 1 }, 5],
                  [{ zoom: 15, value: 62 }, 10],
                  [{ zoom: 22, value: 1 }, 20],
                  [{ zoom: 22, value: 62 }, 50]
                ]
              },
              'circle-color': {
                property: 'carID',
                type: 'exponential',
                stops: [
                  [0, 'rgba(236,222,239,0)'],
                  [10, 'rgb(236,222,239)'],
                  [20, 'rgb(208,209,230)'],
                  [30, 'rgb(166,189,219)'],
                  [40, 'rgb(103,169,207)'],
                  [50, 'rgb(28,144,153)'],
                  [60, 'rgb(1,108,89)']
                ]
              },
              'circle-stroke-color': 'white',
              'circle-stroke-width': 1,
              'circle-opacity': {
                stops: [
                  [14, 0],
                  [15, 1]
                ]
              }
            }
          },
          'waterway-label'
        );
        map.on('click', 'airports-point', ({ features }) => {
          new mapboxgl.Popup()
            .setLngLat(features[0].geometry.coordinates)
            .setHTML(`<strong>carID:</strong> ${features[0].properties.carID}`)
            .addTo(map);
        });

                });    
            });
        }
        </script>
        </body>
        </html>
        """

        # data_path="'/Users/418mac/Documents/nikkipei/Attain3-self/videoData/DJI_0002stab_latlng.csv'"
        chi = "url:"
        inde = hh.find(chi)
        b = list(hh)
        b.insert(inde + len(chi), "'{csv_path}'")
        b = "".join(b)

        webEngineView.setHtml(b)
        # webEngineView.setHtml(hh)

        dataVS.addWidget(webEngineView)

    
        # dataVS.addWidget(webEngineView)


def onOpenVideo():
    path, _ = QFileDialog.getOpenFileName(
        window,
        "Open video",
        filter="All files (*.*)",
    )
    if path:
        print(f"Loading video: {path}")
        player.load(path)


def onSaveCSV():
    global csv_path
    if csv_path:
        print(f"Saving CSV: {csv_path}")
        data = editor.getData()
        # print(data)
        saveCSV(csv_path, data)
    else:
        onSaveCSVAs()


def onSaveCSVAs():
    global csv_path
    path, _ = QFileDialog.getSaveFileName(
        window,
        "Save CSV",
        filter="All files (*.*);;CSV (*.csv)",
    )
    if path:
        csv_path = path
        print(f"Saving CSV: {csv_path}")
        data = editor.getData()
        saveCSV(csv_path, data)


def activateTool(tool):
    editor.toggleTool(tool)

    active_tool = editor.getActiveTool()
    # print(active_tool)

    action_add_arc.blockSignals(True)
    action_add_arc.setChecked(active_tool == TOOL_ADD_ARC)
    action_add_arc.blockSignals(False)

    action_add_region.blockSignals(True)
    action_add_region.setChecked(active_tool == TOOL_ADD_REGION)
    action_add_region.blockSignals(False)


action_open_csv.triggered.connect(onOpenCSV)
action_open_video.triggered.connect(onOpenVideo)
action_save_csv.triggered.connect(onSaveCSV)
action_save_csv_as.triggered.connect(onSaveCSVAs)
action_quit.triggered.connect(lambda: QApplication.quit())
action_add_arc.toggled.connect(lambda: activateTool(TOOL_ADD_ARC))
action_remove_arc.triggered.connect(lambda: activateTool(TOOL_REMOVE_ARC))
action_add_region.toggled.connect(lambda: activateTool(TOOL_ADD_REGION))
action_remove_region.triggered.connect(lambda: activateTool(TOOL_REMOVE_REGION))
action_zoom_in.triggered.connect(editor.zoomIn)
action_zoom_out.triggered.connect(editor.zoomOut)


frames_slider.valueChanged.connect(player.setFrame)
frame_spin_box.valueChanged.connect(player.setFrame)

# web engine View
dataVS = window.findChild(QVBoxLayout, "webpage")
webEngineView = QWebEngineView()

# hh = """
# <!DOCTYPE html>
# <html>
# <head>
# <meta charset="utf-8">
# <title>Display buildings in 3D</title>
# <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
# <link href="https://api.mapbox.com/mapbox-gl-js/v2.4.1/mapbox-gl.css" rel="stylesheet">
# <script src="https://api.mapbox.com/mapbox-gl-js/v2.4.1/mapbox-gl.js"></script>
# <script src='csv2geojson.js'></script>
# <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>

# <style>
# body { margin: 0; padding: 0; }
# #map { position: absolute; top: 0; bottom: 0; width: 100%; }
# </style>
# </head>
# <body>
# <div id="map"></div>
# <script>
# mapboxgl.accessToken = 'pk.eyJ1IjoiZGFuc3dpY2siLCJhIjoiY2l1dTUzcmgxMDJ0djJ0b2VhY2sxNXBiMyJ9.25Qs4HNEkHubd4_Awbd8Og';
# var map = new mapboxgl.Map({
#     container: 'map', // container id
#     style: 'mapbox://styles/mapbox/streets-v8', //stylesheet location
#     center: [ 113.048778519374, 28.1721735387714], // starting position
#     zoom: 10 // starting zoom
#     // center: [ -89.89709901792442, 41.29146740952274], // starting position
#     // zoom: 3 // starting zoom
# });

# $(document).ready(function() {
#     $.ajax({
#         type: "GET",
#         url: 
#         // url: './DJI_0002stab_latlng.csv',

#         dataType: "text",
#         success: function(csvData) {makeGeoJSON(csvData);}
#      });
# });

# function makeGeoJSON(csvData) {
#     csv2geojson.csv2geojson(csvData, {
#         latfield: 'Lat',
#         lonfield: 'Lng',
#         // latfield: 'latitude',
#         // lonfield: 'longitude',
#         delimiter: ','
#     }, function(err, data) {
#         map.on('load', function () {
#             map.addSource('airports', {
#             type: 'geojson',
#             data: data
#           });
#             map.addLayer(
#   {
#     id: 'airports-heat',
#     type: 'heatmap',
#     source: 'airports',
#     maxzoom: 15,
#     paint: {
#       // increase weight as diameter breast height increases
#       'heatmap-weight': {
#         property: 'carID',
#         type: 'exponential',
#         stops: [
#           [1, 0],
#           [62, 1]
#         ]
#       },
#       // increase intensity as zoom level increases
#       'heatmap-intensity': {
#         stops: [
#           [11, 1],
#           [15, 3]
#         ]
#       },
#       // assign color values be applied to points depending on their density
#       'heatmap-color': [
#         'interpolate',
#         ['linear'],
#         ['heatmap-density'],
#         0,
#         'rgba(236,222,239,0)',
#         0.2,
#         'rgb(208,209,230)',
#         0.4,
#         'rgb(166,189,219)',
#         0.6,
#         'rgb(103,169,207)',
#         0.8,
#         'rgb(28,144,153)'
#       ],
#       // increase radius as zoom increases
#       'heatmap-radius': {
#         stops: [
#           [11, 15],
#           [15, 20]
#         ]
#       },
#       // decrease opacity to transition into the circle layer
#       'heatmap-opacity': {
#         default: 1,
#         stops: [
#           [14, 1],
#           [15, 0]
#         ]
#       }
#     }
#   },
#   'waterway-label'
# );

# map.addLayer(
#   {
#     id: 'airports-point',
#     type: 'circle',
#     source: 'airports',
#     minzoom: 14,
#     paint: {
#       // increase the radius of the circle as the zoom level and dbh value increases
#       'circle-radius': {
#         property: 'carID',
#         type: 'exponential',
#         stops: [
#           [{ zoom: 15, value: 1 }, 5],
#           [{ zoom: 15, value: 62 }, 10],
#           [{ zoom: 22, value: 1 }, 20],
#           [{ zoom: 22, value: 62 }, 50]
#         ]
#       },
#       'circle-color': {
#         property: 'carID',
#         type: 'exponential',
#         stops: [
#           [0, 'rgba(236,222,239,0)'],
#           [10, 'rgb(236,222,239)'],
#           [20, 'rgb(208,209,230)'],
#           [30, 'rgb(166,189,219)'],
#           [40, 'rgb(103,169,207)'],
#           [50, 'rgb(28,144,153)'],
#           [60, 'rgb(1,108,89)']
#         ]
#       },
#       'circle-stroke-color': 'white',
#       'circle-stroke-width': 1,
#       'circle-opacity': {
#         stops: [
#           [14, 0],
#           [15, 1]
#         ]
#       }
#     }
#   },
#   'waterway-label'
# );
# map.on('click', 'airports-point', ({ features }) => {
#   new mapboxgl.Popup()
#     .setLngLat(features[0].geometry.coordinates)
#     .setHTML(`<strong>carID:</strong> ${features[0].properties.carID}`)
#     .addTo(map);
# });

#         });    
#     });
# }
# </script>
# </body>
# </html>
# """

# chi = "url:"
# inde = hh.find(chi)
# b = list(hh)
# b.insert(inde + len(chi), "'./airports3.csv',")
# b = "".join(b)

# webEngineView.setHtml(b)
# # webEngineView.setHtml(hh)

# dataVS.addWidget(webEngineView)


def onLoad():
    frames_slider.setRange(0, player.frame_count - 1)
    frames_count_label.setText(f"/ {player.frame_count-1}")
    frame_spin_box.setRange(0, player.frame_count - 1)


def onFrame(
    player_x,
    player_y,
    player_w,
    player_h,
    frame_w,
    frame_h,
    frame_index,
    pixmap,
):
    editor.setFramePixmap(
        player_x,
        player_y,
        player_w,
        player_h,
        frame_w,
        frame_h,
        frame_index,
        pixmap,
    )

    frames_slider.blockSignals(True)
    frames_slider.setValue(frame_index)
    frames_slider.blockSignals(False)

    frame_spin_box.blockSignals(True)
    frame_spin_box.setValue(frame_index)
    frame_spin_box.blockSignals(False)


player.onLoad = onLoad
player.onFrame = onFrame
player.onResize = editor.setGeometry

# player.load("../data/DJI_0543.MP4")
# player.play()

# data = loadCSV("../data/DJI_0543stab.csv")
# editor.setData(data)

# save_csv("../test.csv", data)

window.show()
app.exec_()
