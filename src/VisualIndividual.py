from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import cv2
import numpy as np
import pandas as pd
import pyqtgraph as pg
import math
import mpu
from haversine import haversine
from PyQt5.QtWebEngineWidgets import QWebEngineView

class VisualIndividual(QWidget):
    def __init__(self, visualGraphicsView, visualverticalLayout, visualTrajectverticalLayout, visualHeadwayverticalLayout, 
                visualPreFramebtn,visualNextFramebtn, visualSlider,visualLabel, carIDdisplay, carTypeDisplay,playBtn, 
                pauseBtn, stopBtn, laneWebEngineView, parent=None):
        super().__init__(parent)
        frame = 0
        width = 400
        height = 300
        self.graphWidgetSpeed = pg.PlotWidget()
        self.graphWidgetSpeed.setFixedWidth(width)
        self.graphWidgetSpeed.setFixedHeight(height)

        self.graphWidgetSpeed.setLabel('left', 'Speed (MPH)')
        self.graphWidgetSpeed.setLabel('bottom', 'Time (S)')
        self.graphWidgetSpeed.showGrid(x=True, y=True)
        visualverticalLayout.addWidget(self.graphWidgetSpeed)

        self.graphWidgetTraject = pg.PlotWidget()
        self.graphWidgetTraject.setFixedWidth(width)
        self.graphWidgetTraject.setFixedHeight(height)


        self.graphWidgetTraject.setLabel('left', 'Acceleration (m/s^2)')
        self.graphWidgetTraject.setLabel('bottom', 'Time (S)')
        self.graphWidgetTraject.showGrid(x=True, y=True)
        visualTrajectverticalLayout.addWidget(self.graphWidgetTraject)

        # self.graphWidgetHead = pg.PlotWidget()
        # self.graphWidgetHead.setFixedWidth(width)
        # self.graphWidgetHead.setFixedHeight(height)
        
        # visualHeadwayverticalLayout.addWidget(self.graphWidgetHead)
        # visualHeadwayverticalLayout.hide()

        visualGraphicsView.setScene(QtWidgets.QGraphicsScene(self))

        path = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/DJI_Orig.mp4'
        vidcap = cv2.VideoCapture(path)
        visualSlider.valueChanged.connect(self.changed_slider1)
        # visualNextFramebtn.clicked.connect(lambda:self.nextFrame(self.visualSlider.value()))
        self.visualverticalLayout = visualverticalLayout
        self.visualLabel = visualLabel
        self.vidcap = vidcap
        self.visualSlider = visualSlider
        self.visualGraphicsView = visualGraphicsView
        self.visualGraphicsView.viewport().installEventFilter(self)
        self.carIDdisplay = carIDdisplay
        self.carTypeDisplay = carTypeDisplay

        visualPreFramebtn.clicked.connect(self.preFrame)
        visualNextFramebtn.clicked.connect(self.nextFrame)

        self.runable = True
        playBtn.clicked.connect(lambda:self.playFun(self.visualSlider.value()))
        pauseBtn.clicked.connect(self.pauseFun)
        stopBtn.clicked.connect(lambda:self.displayImage(frame))
        self.htmlText()
        self.playBtn = playBtn
        html = self.htmlText()
        laneWebEngineView.setHtml(html)
        self.displayImage(frame)
    def eventFilter(self, o, e):
        if self.visualGraphicsView.viewport() is o:
            if e.type() == QEvent.MouseButtonPress:
                if e.buttons() & Qt.LeftButton:
                    print("press1")
                    scene_pos = self.visualGraphicsView.mapToScene(e.pos())
                    item = self.visualGraphicsView.scene().itemAt(QPointF(scene_pos), QTransform())
                    if type(item) is QGraphicsPixmapItem:
                        mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                        # print(mouseX)
                        newx = int(mouseX/0.28)
                        newy = int(mouseY/0.28)
                        # print(newx)
                        for i in range(0, len(self.userid)):
                            # print(self.userid['carCenterX'].values[i], 'self.userid.values[i]')
                            # print((self.userid['carCenterX'].values[i])-20,(self.userid['carCenterX'].values[i])+20 , 'id: ', self.userid['carID'].values[i])
                            #check click is inside the point
                            if newx in range((self.userid['carCenterX'].values[i])-20,(self.userid['carCenterX'].values[i])+20 ):
                                if newy in range((self.userid['carCenterY'].values[i])-20,(self.userid['carCenterY'].values[i])+20 ):
                                    print(self.userid['carID'].values[i])
                                    
                                    selectcarID = self.userid['carID'].values[i]
                                    self.carIDdisplay.setText(str(selectcarID))
                                    self.carTypeDisplay.setText('Compact Car')
                                    self.graphWidgetSpeed.clear()
                                    self.graphWidgetTraject.clear()

                                    # find the avg speed
                                    self.displayTrajectory(selectcarID)
                                    speed, time = self.eachAvgSpeed(selectcarID)
                                    pen = pg.mkPen(color= 'c', width=3)
                                    # self.graphWidgetSpeed.setYRange(0,max[speed], padding = 0)
                                    self.graphWidgetSpeed.plot(time, speed, name="Speed",  pen=pen, 
                                        symbol='o', symbolSize=7, symbolBrush=('c'),padding = 0)


                                    # find the acceleration
                                    t = 1 # 60 frames to 1 second
                                    acceleration, actime = self.findAcceleartion(speed, t)
                                    pen1 = pg.mkPen(color= 'y', width=3)
                                    print(acceleration)
                                    print(actime)
                                    self.graphWidgetTraject.plot(actime, acceleration, name="Acceleration",  pen=pen1, 
                                        symbol='o', symbolSize=7, symbolBrush=('y'),padding = 0)
                                    break

        return super().eventFilter(o, e)

    def findSpeed (self, frame, lat1, lon1, lat2, lon2):
        dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
        miles = dist*0.6214
        # sec = frame/30
        hr = 1/3600
        speed = (miles/hr)
        print(lat1, lon1, lat2, lon2)
        print(speed, miles)
        #find velocity
        # velocity = miles/ 1 #t=1 sec

        return speed

    def findAcceleartion(self, speed, t):
        
        # t = 1 // from intial to final using 1 second
        acceleartionlist = []
        time = 1
        actime = []
        print(speed)
        for i in range(0, len(speed)):
            if i == len(speed)-1:
                # actime.append(time)
                break
            # convert miles to meter per second
            initialSpeed = speed[i]/2.237
            finalSpeed = speed[i+1]/2.237

            acceleartion = (finalSpeed- initialSpeed)/t
            acceleartionlist.append(int(acceleartion)) 
            actime.append(time)
            time+=1
        print(acceleartionlist)
        return acceleartionlist, actime
    # def findVelocity(self, distance, )

    def displayTrajectory(self, selectcarID):
        trajectoryid = self.df[self.df['carID']==selectcarID]
        trajectX = trajectoryid['carCenterX'].values.tolist()
        trajectY = trajectoryid['carCenterY'].values.tolist()
        print('carCenterX')
        print(trajectoryid)
        print(trajectX)
        print(trajectY)

        image = self.trajectoryimg.copy()

        for i in range(0, len(trajectX), 15):
            image = cv2.circle(image, (trajectX[i], trajectY[i]), 0, (0, 255, 0), 15)
        scale_percent = 28
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # print(dim,'dim')
        # dim = (1200,800)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 
        self.visualGraphicsView.scene().clear()
        self.visualGraphicsView.scene().addPixmap(pix)

    def eachAvgSpeed(self, selectcarID):
        fps2 = self.vidcap.get(5)
        print(fps2, 'fps2')
        frameSecds = fps2 *1 # avg of every sec

        carid = self.df[self.df['carID']==selectcarID]

        # find every second (60 fps) speed for seletcted car id
        rangeFrame = (carid['frameNUM'].values[-1])-(carid['frameNUM'].values[0])
        numTime = math.floor(rangeFrame/frameSecds )
        print(rangeFrame,'rangeFrame')
        print(numTime,'numTime')
        avgTime = []
        array = []

        a = carid[(carid['carID']==3)]
        print(a)
        for x in range(0, numTime):

            # from 0 --61
            frame = carid[(carid['frameNUM']>= carid['frameNUM'].values[0]+(frameSecds*x)) & (carid['frameNUM']<= carid['frameNUM'].values[0]+(frameSecds*(x+1)))]

            speed = self.findSpeed(fps2, frame['lat'].values[0], frame['lon'].values[0], frame['lat'].values[-1], frame['lon'].values[-1] )
       
            array.append(int(speed))
            avgTime.append(x+1)

        return array, avgTime


    def playFun(self,frameNumber):
        self.runable = True
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        self.playBtn.setEnabled(False)
        while True:
            if not self.runable:
                self.visualSlider.setValue(frameNumber-2)
                # self.visualLabel.setText(str(frameNumber-2))
                break
            success,image = self.vidcap.read()
            image = cv2.putText(
                      img = image,
                      text = str(frameNumber),
                      org = (50,100),
                      fontFace = cv2.FONT_HERSHEY_SIMPLEX ,
                      fontScale = 3,
                      color = (255, 0, 0),
                      thickness = 3)
            userid = self.df[self.df['frameNUM']==frameNumber]

            if len(userid)>0:
                for i in range(0, len(userid)):
                    cx = userid['carCenterX'].values[i]
                    cy = userid['carCenterY'].values[i]
                    image = cv2.circle(image, (cx, cy), 0, (255, 255, 0), 30)
                    image = cv2.putText(
                              img = image,
                              text = str(userid['carID'].values[i]),
                              org = (cx+15,cy+10),
                              fontFace = cv2.FONT_HERSHEY_SIMPLEX ,
                              fontScale = 3,
                              color = (255, 255, 0),
                              thickness = 3)

            scale_percent = 28 # percent of original size

            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            # print(dim,'dim')
            # dim = (1200,800)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

            b,g,r = cv2.split(image)           # get b, g, r
            rgb_img1 = cv2.merge([r,g,b])

            height, width, channel = rgb_img1.shape
            bytesPerLine = 3 * width
            qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap(qImg) 
            self.visualGraphicsView.scene().clear()
            self.visualGraphicsView.scene().addPixmap(pix)
            # self.visualSlider.setValue(frameNumber)
            # self.visualLabel.setText(str(frameNumber))
            QApplication.processEvents()
            self.visualLabel.setText(str(frameNumber+1))
            frameNumber+=1

    def pauseFun(self):
        self.runable = False
        self.playBtn.setEnabled(True)

    def nextFrame(self):
        self.pauseFun()
        value = self.visualSlider.value()
        if value < self.frameTotal:
            value+=1
            self.visualSlider.setValue(value)
            self.visualLabel.setText(str(value))
            self.displayImage(self.visualSlider.value())


    def preFrame(self):
        self.pauseFun()
        
        value = self.visualSlider.value()
        if value > 0:
            value-=1
            self.visualSlider.setValue(value)
            self.visualLabel.setText(str(value))
            self.displayImage(self.visualSlider.value())

    def changed_slider1(self):
        self.pauseFun()

        value = self.visualSlider.value()
        self.visualLabel .setText(str(value))
        self.displayImage(self.visualSlider.value())

    def displayImage(self, frameNumber):
        self.visualSlider.setValue(frameNumber)
        self.visualLabel.setText(str(frameNumber))


        self.df = pd.read_csv("/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/TTCGPS.csv", sep=',')
        
        
        print(frameNumber,'frameNumber')
        
        
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        # fps2 = self.vidcap.get(5)
        # fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        # print(fps2,'fps2')
        # print(fps,'fps')
        success,image = self.vidcap.read()

        self.userid = self.df[self.df['frameNUM']==frameNumber]
        # print(self.userid, 'self.userid')
        image = cv2.putText(
                  img = image,
                  text = str(frameNumber),
                  org = (50,100),
                  fontFace = cv2.FONT_HERSHEY_SIMPLEX ,
                  fontScale = 3,
                  color = (255, 0, 0),
                  thickness = 3)
        #draw each car center:
        if len(self.userid)>0:
            for i in range(0, len(self.userid)):
                cx = self.userid['carCenterX'].values[i]
                cy = self.userid['carCenterY'].values[i]
                image = cv2.circle(image, (cx, cy), 0, (255, 255, 0), 30)
                image = cv2.putText(
                          img = image,
                          text = str(self.userid['carID'].values[i]),
                          org = (cx+15,cy+10),
                          fontFace = cv2.FONT_HERSHEY_SIMPLEX ,
                          fontScale = 3,
                          color = (255, 255, 0),
                          thickness = 3)

                # print(cx, cy, 'id: ', self.userid['carID'].values[i])
        scale_percent = 28 # percent of original size

        self.trajectoryimg = image.copy()

        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # print(dim,'dim')
        # dim = (1200,800)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 
        self.visualGraphicsView.scene().clear()
        self.visualGraphicsView.scene().addPixmap(pix)

        self.frameTotal = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

        self.visualSlider.setMaximum(self.frameTotal-1)


    def htmlText(self):
        html = ''' 
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Display buildings in 3D</title>
<meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://api.mapbox.com/mapbox-gl-js/v2.7.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v2.7.0/mapbox-gl.js"></script>
<style>
body { margin: 0; padding: 0; }
#map { position: absolute; top: 0; bottom: 0; width: 100%; }
</style>
</head>
<body>
<div id="map"></div>
<script>
    // TO MAKE THE MAP APPEAR YOU MUST
    // ADD YOUR ACCESS TOKEN FROM
    // https://account.mapbox.com
    mapboxgl.accessToken = 'pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoiY2pudzRtaWloMDAzcTN2bzN1aXdxZHB5bSJ9.2bkj3IiRC8wj3jLThvDGdA';
const map = new mapboxgl.Map({
style: 'mapbox://styles/mapbox/light-v10',
center: [-81.20587074, 28.60311182],
zoom: 18,
pitch: 45,
bearing: -17.6,
container: 'map',
antialias: true
});
 
map.on('load', () => {
// Insert the layer beneath any symbol layer.
const layers = map.getStyle().layers;
const labelLayerId = layers.find(
(layer) => layer.type === 'symbol' && layer.layout['text-field']
).id;
 
// The 'building' layer in the Mapbox Streets
// vector tileset contains building height data
// from OpenStreetMap.
map.addLayer(
{
'id': 'add-3d-buildings',
'source': 'composite',
'source-layer': 'building',
'filter': ['==', 'extrude', 'true'],
'type': 'fill-extrusion',
'minzoom': 15,
'paint': {
'fill-extrusion-color': '#aaa',
 
// Use an 'interpolate' expression to
// add a smooth transition effect to
// the buildings as the user zooms in.
'fill-extrusion-height': [
'interpolate',
['linear'],
['zoom'],
15,
0,
15.05,
['get', 'height']
],
'fill-extrusion-base': [
'interpolate',
['linear'],
['zoom'],
15,
0,
15.05,
['get', 'min_height']
],
'fill-extrusion-opacity': 0.6
}
},
labelLayerId
);
});
</script>
 
</body>
</html>


        '''
        return html

