from dataclasses import dataclass
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from typing import List, Dict
import pandas as pd
import sys, csv
import math
import mpu

import cv2  # Not actually necessary if you just want to create an image.
import numpy as np
from numpy.linalg import inv
import geopy
from math import sin, cos, radians, pi
from geopy.distance import geodesic
import cv2
import math
from math import *
import os
import shutil
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from bokeh.models.glyphs import Text
from numpy.linalg import inv
from bokeh.models import BoxZoomTool
from bokeh.plotting import figure, output_notebook, show
from bokeh.io import export_png
import pandas as pd
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from bokeh.models import ColumnDataSource

from bokeh.models import GMapOptions
from bokeh.plotting import gmap
from bokeh.io import export_png


uwbPoints = []
# gpsPoints = []


class Convertor(QWidget):
    def __init__(self, player, path, video_parentGPS, vbox, verifyMapbtn, convertResLabel, convPointsLabel, xy_save_btn, editConv, deleteConv, parent=None):
        super().__init__(parent)

        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.setContentsMargins(0, 0, 0, 0)

        # self.setMouseTracking(True)

        vidcap = cv2.VideoCapture(path)
        success,image = vidcap.read()
        count = 0

        # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file  

        success,image = vidcap.read()

        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        # print(success,"zai html limian de image")
        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg)
        pixmap4 = pix.scaled(453, 186, Qt.KeepAspectRatio)
        print(qImg)
        
        scene = QGraphicsScene(QRectF(self.rect()), self)

        video_pixmap = QGraphicsPixmapItem(pix)
        video_pixmap.setZValue(-100)

        scene.addItem(video_pixmap)

        view = QGraphicsView(scene, self)
        view.setFrameStyle(QFrame.NoFrame)
        view.setFrameShape(QFrame.Shape.NoFrame)
        view.setFrameShadow(QFrame.Shadow.Plain)
        view.setContentsMargins(0, 0, 0, 0)
        view.setViewportMargins(QMargins(0, 0, 0, 0))
        view.setStyleSheet("border-width: 0; border-color: transparent")
        # view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        print(type(xy_save_btn))

        print(scene.width(),'width')
        print(scene.height(),'height')

        xy_save_btn.setEnabled(True)
        xy_save_btn.clicked.connect(self.outputBtnFunc)
        self.xy_save_btn = xy_save_btn
        print(type(xy_save_btn))

        editConv.setEnabled(True)
        editConv.clicked.connect(self.savebtnFuncTest)
        self.editConv = editConv

        deleteConv.setEnabled(True)
        deleteConv.clicked.connect(self.deleteConvFunc)
        self.deleteConv = deleteConv

        self.verifyMapbtn = verifyMapbtn
        self.convertResLabel = convertResLabel

        # self.pixmap4 = pixmap4
        self.pix = pix

        self.convPointsLabel = convPointsLabel

        self.video_parentGPS = video_parentGPS

        self.gpsPoints = [] 
        self.tempout = []

        self.vbox = vbox

        self.player = player


        self.scene = scene
        self.video_pixmap = video_pixmap
        self.view = view



    def mouseDoubleClickEvent(self, event):
        print('event.pos():' , event.pos())
        count = 0
        scene_pos = self.view.mapToScene(event.pos())
        print('scene_pos: ',scene_pos)
        print('QPointF(scene_pos): ', QPointF(scene_pos))

        item = self.scene.itemAt(QPointF(scene_pos), QTransform())
        if type(item) is QGraphicsPixmapItem:
            ellipse = QGraphicsEllipseItem(-5, -5, 10, 10)
            ellipse.setPos(scene_pos)
            brush = QBrush(Qt.blue)
            ellipse.setBrush(brush)
            self.scene.addItem(ellipse)
            ellipse.setFlag(QGraphicsItem.ItemIsMovable, True)
            ellipse.setFlag(QGraphicsItem.ItemIsSelectable, True)
            ellipse.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True);
            # print(ellipse.pos())
            # print(scene_pos)
            # x, y = event.pos().x(), event.pos().y()
            # uwbPoints.append([x,y])  
            input, ok = QInputDialog.getText( self, "Enter Coordinates", "Enter New Coordinates as 'xcoord, ycoord'")

            if ok:
                x = input.split( "," )[ 0 ]
                x1 = float(x)

                y = input.split( "," )[ 1 ]
                y1 = float(y)
      
                if not x:
                    print ("Ooops!X value is missing!")
                if not y:
                    print ("Ooops!Y value is missing!")

            
                # print(self.clickMethodeditor(x, y))
                self.gpsPoints.insert(0, [x1,y1])
                self.loadOutputLabel()
                    # print('gpsPoints')

                    # print(self.gpsPoints)
            else:
                self.scene.removeItem(ellipse)
                self.loadOutputLabel()

    def verifyMapFun(self, df_new):

        print('lon', df_new.lon[0])
        print('lat', df_new.lat[1])
        plot_width  = int(1800)
        plot_height = int(2000)

        map_options = GMapOptions(lat=df_new.lat[1], lng=df_new.lon[0], map_type="hybrid", zoom=20)


        p = figure(plot_width=plot_width, plot_height=plot_height, title="Linear Color Map Based on Y")
        p = gmap("AIzaSyDl07i6O-6BiKhPIzNjgdmXiDR4EtqvDfo", map_options = map_options)


        source = ColumnDataSource(dict(x=df_new.lon, z=df_new.lat))
        mapper = linear_cmap(field_name='y', palette=Spectral6 ,low=0 ,high=2)

        p.circle(x='x', y='z',color='red', source=source,size=6)
        #p.legend()
        #p.circle(x='x', y='z',color='red', size="sizes", source=source,fill_color='white', fill_alpha=0.8)
        p.xaxis.visible = False
        p.yaxis.visible = False
        # export_png(p, filename="1011_figure.png")


        show(p)





    def loadOutputLabel(self):
        self.uwbPoints1 = []
        count = 0

        #edit btn 选择which points in dialog
        self.items1 = []

        #label points
        self.items2 = []

        for item in self.scene.items()[:-1] :
            x, y = int(item.pos().x()), int(item.pos().y())
            self.uwbPoints1.append([x,y])
            count+=1
            self.items1.append(str(count))
            self.items2.insert(0,count)
       
        print('items1 in output label: ', self.items1)
        print('items2 in output label: ', self.items2)
        self.loadPointsTextFunc()

    def loadPointsTextFunc(self):
        for i in range(len(self.gpsPoints)):
            print(self.gpsPoints)

            count = 5 # every 3 rows in a loop
            index = 5*i

            self.vbox.addWidget(QLabel('Point '+ str(self.items2[i]) +': '), index, 0)

            self.vbox.addWidget(QLabel('Pixcel:'), index+1, 0)
            self.vbox.addWidget(QLabel(str(self.uwbPoints1[i])), index+1, 1)

            print('i 现在是这个了！！！！！！！！！！------>',[i])

            print('self.gpsPoints[',i,'][',i,']) ',self.gpsPoints[i][0])
            print('self.gpsPoints[',i,'][',i+1,']) ',self.gpsPoints[i][1])


            self.vbox.addWidget(QLabel('GPS Lat:'), index+2, 0)
            globals()[f"lineObjectLat{i}"] = QLineEdit()
            globals()[f"lineObjectLat{i}"].setText(str(self.gpsPoints[i][0]))
            globals()[f"lineObjectLat{i}"].setStyleSheet('background-color: white; color: black')
            self.vbox.addWidget(globals()[f"lineObjectLat{i}"], index+2, 1)

            self.vbox.addWidget(QLabel('GPS Lon:'), index+3, 0)
            globals()[f"lineObjectLon{i}"] = QLineEdit()
            globals()[f"lineObjectLon{i}"].setText(str(self.gpsPoints[i][1]))
            globals()[f"lineObjectLon{i}"].setStyleSheet('background-color: white; color: black')
            self.vbox.addWidget(globals()[f"lineObjectLon{i}"], index+3, 1)
            print(111111111111122222222222222222222)
            print(type(lineObjectLat0))
            self.vbox.addWidget(QLabel(' '), index+4, 0)

            QLabel().setStyleSheet('color: white;')

        self.vbox.setRowStretch(100, 1)

    def savebtnFuncTest (self):
        print('you have pressed saved button')
        # print(lineObjectLat0.text())
        for i in range(len(self.gpsPoints)):
            lat = globals()[f"lineObjectLat{i}"].text()
            lon = globals()[f"lineObjectLon{i}"].text()
            print('type:', type(lat))
            print(self.gpsPoints[i])
            self.gpsPoints[i] = ([float(lat),float(lon)])
            print(self.gpsPoints)
        self.loadOutputLabel()


    def outputLabelFunc(self, tempout):

        str1 = ''
        for i in range(len(tempout)):
            str1 +=  """
Point {}:
Converted: {}
                        """.format(self.items2[i], tempout[i])
            print('gps:', tempout)
            self.convertResLabel.clear()
            self.convertResLabel.appendPlainText(str1) 



    def deleteConvFunc(self):
        item, ok = QInputDialog().getItem(self, "QInputDialog().getItem()",
                                     "Select Point to Delete:", self.items1, 0, False)

        if ok:
            for item111 in self.scene.items():
                print('==============before========',item111.pos())
            print('delete function called -------------')

            print('选择的点： ',int(item)+1)
            index = -(int(item)+1)
            print(index)
            print(type(index))
            pos = self.scene.items()[index]
            print('这里是pos的值for removeItem in scene', pos)
            self.scene.removeItem(pos)
            for item111 in self.scene.items():
                print('===============after========',item111.pos())
            self.gpsPoints.pop(-int(item))
            print(pos.pos())
            print('pxicel points after delete: ',self.uwbPoints1)
            print('gps points after delete', self.gpsPoints)
            for i in reversed(range(self.vbox.count())): 
                self.vbox.itemAt(i).widget().deleteLater()
            self.loadOutputLabel()

    def outputBtnFunc(self):
        print('pxicel points after delete: ',self.uwbPoints1)
        print('gps points after delete', self.gpsPoints)
        gpsPoints = self.gpsPoints
        uwbPoints = self.uwbPoints1
        tempout = []
        inttempout=[]
        if len(self.gpsPoints)>3 :
                startLat = self.gpsPoints[0][0]
                startLon = self.gpsPoints[0][1]
                startX = self.uwbPoints1[0][0]
                startY = self.uwbPoints1[0][1]
                # print('startLat: ')
                # print(startLat, startLon, startX, startY)
                gpsPointsInUwb=[]
                for i in range(len(self.gpsPoints)):
                    dist=getDistance(startLat, startLon,self.gpsPoints[i][0], self.gpsPoints[i][1])
                    bearing = getBearing(startLat, startLon,self.gpsPoints[i][0], self.gpsPoints[i][1])
                    newX,newY=getNextPointFromBearingDistance(startX,startY,dist,180-bearing)
                    gpsPointsInUwb.append((newX,newY))
                pts1 = np.float32(gpsPointsInUwb)
                pts2 = np.float32(self.uwbPoints1)
                print('pts1')
                print(pts1)
                print('pts2')
                print(pts2)
                M = cv2.findHomography(pts1,pts2)
                for i in range(len(self.uwbPoints1)):
                    tp1=getTranformedPoints(self.uwbPoints1[i][0],self.uwbPoints1[i][1],M[0])
                    tmpAngel=angle_to(tp1,(startX,startY))
                    tmpdist=getDistFromTwoPoints(startX,startY,tp1[0],tp1[1])
                    tmpLat1,tmpLon1=getNextGPSPointFromBearingDistance(startLat,startLon,tmpdist,tmpAngel)
                    # print(type(tmpLat1))
                    # print(str(tmpLat1))
                    # tempout.append([str(tmpLat1),str(tmpLon1)])
                    tempout.append([(tmpLat1),(tmpLon1)])

                    inttempout.append([(tmpLat1),(tmpLon1)])
                    # tempout.append(str(tmpLon1))

                    # print(tmpLat1,tmpLon1)
                    print("tmpout: ")
                    print(tempout)
                df_new = pd.DataFrame(inttempout, columns=['lat', 'lon'])
                self.verifyMapbtn.setEnabled(True)
                self.verifyMapbtn.clicked.connect(lambda: self.verifyMapFun(df_new))
                self.outputLabelFunc(tempout)
    ###########lab 



    def resizeEvent(self, event):
        if len(self.gpsPoints)>=1:
            print(self.gpsPoints, '@@@@@@@@@@@@@@@@@')
            del self.gpsPoints[:]
            for i in reversed(range(self.vbox.count())): 
                self.vbox.itemAt(i).widget().setParent(None)
            self.loadOutputLabel()

        width, height = event.size().width(), event.size().height()
        self.view.resize(width, height)
        self.view.setSceneRect(QRectF(self.view.contentsRect()))
        print(1)
        print(self.video_parentGPS.width(), 'video_parentGPS width')
        print(self.video_parentGPS.height(), 'video_parentGPS height')
        pixmap4 = self.pix.scaled(self.video_parentGPS.width(), self.video_parentGPS.height(), Qt.KeepAspectRatio)
        video_pixmap = QGraphicsPixmapItem(pixmap4)
        video_pixmap.setZValue(-100)
        video_pixmap.setPos(0, 100)
        # print(self.scene.items()[-1], 'position[0]')
        # item = self.scene.items()[-1]
        self.scene.clear()
        self.scene.addItem(video_pixmap)
        # self.scene.removeItem(item)

        for item in self.scene.items():
            print(item, 'resieze')

def findSpeed (frame, lat1, lon1, lat2, lon2):
    dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    miles = dist*0.6214
    sec = frame/30
    hr = sec/3600
    speed = miles/hr
    return speed

def speedVolume(path):
    df = pd.read_csv(path, index_col=False, usecols=['frameNUM','carID','Lat','Lng'])
    # carid = df[(df['Lat']==28.17217354) &(df['Lng']==113.0487785) ]
    array = []
    numTime = ((df['frameNUM'].max())/30)/30  #number of 30 seconds, 4 times

    for x in range(1, int(numTime)+1):
        secOftime = 900 * x
        frame = df[(df['frameNUM']==secOftime)]
        countCar = frame['carID'].max()
        array.append([30*x, countCar, frame['Lng'].values[-1], frame['Lat'].values[-1]])
    return array

def getBearing(lat1,lon1,lat2,lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = np.rad2deg(math.atan2(y, x));
    if brng < 0: brng+= 360
    return brng
def getDistance(lat1,lon1,lat2,lon2):
    p1 = (lat1,lon1)
    p2 = (lat2,lon2)
    dist=geodesic(p1, p2).m
    return dist
def getNextGPSPointFromBearingDistance(lat1,lon1,dist,bearing):
    origin = geopy.Point(lat1, lon1)
    destination = geodesic(kilometers=dist/1000).destination(origin, bearing)
    lat2, lon2 = destination.latitude, destination.longitude
    return lat2, lon2
def getNextPointFromBearingDistance(x,y,d,theta):
    theta_rad = pi/2 - radians(theta)
    x1=x + d*cos(theta_rad)
    y1=y + d*sin(theta_rad)
    return x1,y1
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
    #uncommit for ubuntu
    #if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX,mouseY = x,y
        print(x,y)
        points.append((mouseX,mouseY))
    if event == cv2.EVENT_RBUTTONDOWN:
    #uncommit for ubuntu
    #if event == cv2.EVENT_RBUTTONDBLCLK:
        mouseX,mouseY = x,y
        if(len(points)>=0):
            points.pop()
def findNewpoint(inputX,inputY,h):
    #转换这个点坐标为np数组
    newPoint=np.array([inputX,inputY,1],np.float32)
    #计算应用矩阵后的点坐标矩阵
    newpoinMatrix = h.dot(newPoint)
    #新坐标点矩阵转换为2d坐标
    outputX=newpoinMatrix[0]/newpoinMatrix[2]
    outputY=newpoinMatrix[1]/newpoinMatrix[2]
    return (outputX,outputY)
def getTranformedPoints(inputX,inputY,M):
    tmpPoint=np.array([inputX,inputY,1],np.float32)
    invM = inv(M)
    tmpPoint2 = invM.dot(tmpPoint)
    #print(tmpPoint2)
    x=tmpPoint2[0]/tmpPoint2[2]
    y=tmpPoint2[1]/tmpPoint2[2]
    return (x,y)

def click_event(event, x, y, flags, params):
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        print(x, ' ', y)

    # # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
  
def getDistFromTwoPoints(x1,y1,x2,y2):
    return math.hypot(x2 - x1, y2 - y1)
def angle_to(p1, p2,clockwise=False):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    angle = degrees(atan2(x, y))
    if clockwise:
        return angle if angle > 0 else angle + 360
    else:
        angle = (360 - angle if angle > 0 else -1 * angle)
        return angle if angle > 0 else angle + 360

