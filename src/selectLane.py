from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import matplotlib.path as mplPath
import pandas as pd

import cv2
import cv2 as cv
import numpy as np
import random
class SelectLane(QWidget):
    def __init__(self, lineSelectGV, laneAddBtn, laneRedoBtn,laneDeleteBtn, laneFinishBtn, lanerestartBtn, parent=None):
        super().__init__(parent)
        path = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/DJI_Orig.mp4'
        vidcap = cv2.VideoCapture(path)
        success,image = vidcap.read()
        image = cv2.resize(image,(1400,850))
        
        lineSelectGV.setScene(QtWidgets.QGraphicsScene(self))
        # lineSelectGV.scene().addPixmap(pix)
        self.lineSelectGV = lineSelectGV
        self.drawing = False
        self.test = False 
        self.pt1_x , self.pt1_y = None , None
        self.image = image
        self.overlay = image.copy()
        self.color=self.getRandomColor()
        self.lane1 = []
        self.savelane1 = []

        self.pointSrc = []
        self.zones = []
        self.zoneColor = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX 
        self.count = 0
        self.csvpath = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/TTCGPS.csv'
        self.vidcap = vidcap
        self.runable = True
        laneAddBtn.clicked.connect(self.addFun)
        laneRedoBtn.clicked.connect(self.redoFun)
        laneDeleteBtn.clicked.connect(self.deleteFun)
        laneFinishBtn.clicked.connect(self.loadvideo)
        lanerestartBtn.clicked.connect(self.restartFun)
        self.laneAddBtn = laneAddBtn
        self.laneRedoBtn = laneRedoBtn
        self.laneDeleteBtn = laneDeleteBtn
        self.laneFinishBtn = laneFinishBtn
        self.lanerestartBtn = lanerestartBtn

        self.displayImage(image)
        # lineSelectGV.viewport().installEventFilter(self)

    def redoFun(self):
        if(len(self.lane1)>0):
            self.lane1 = self.lane1[:-1]
            # print('========redo========')
            # print(self.lane1)
            # self.color=self.getRandomColor()
            self.overlay = self.image.copy()

            if len(self.lane1) ==0:
                self.displayImage(self.image)
                print('empty')
            for item in self.lane1:
                # print('========item========')
                # print(item)
                for i in range(0, len(item)-1):
                    # print(len(item))
                    pt_x, pt_y = item[i][0], item[i][1]
                    self.drawLane(pt_x, pt_y, item[i+1][0], item[i+1][1], self.overlay, self.image)
                    pt_x, pt_y = item[i+1][0], item[i+1][1]
                    # print(x)
                # break
        # print(1)

    def getRandomColor(self):
        return (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.lineSelectGV.mapToScene(event.pos())
            item = self.lineSelectGV.scene().itemAt(QPointF(scene_pos), QTransform())
            self.tmplane = []
            if type(item) is QGraphicsPixmapItem:            
                mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                # print(mouseX)
                # if self.test == True:
                #     for item in self.lane1:
                #         # print(x)
                #         for x in item:
                #             if mouseX in range(x[0]-25, x[0]+25) and mouseY in range(x[1]-20, x[1]+20):
                #                 print('inside')
                #                 break
                # if self.test == False:     
                self.drawing=True
                self.pt1_x, self.pt1_y=mouseX,mouseY
                self.pointSrc.append((mouseX,mouseY))
                self.drawpolyline(self.image)
        if event.button() == Qt.RightButton:
            scene_pos = self.lineSelectGV.mapToScene(event.pos())
            item = self.lineSelectGV.scene().itemAt(QPointF(scene_pos), QTransform())
            self.tmplane = []
            if type(item) is QGraphicsPixmapItem:
                mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                print(mouseX,mouseY, 'mouseX,mouseY')
                print(self.saveFun(mouseX,mouseY))

    def restartFun(self):
        self.lineSelectGV.scene().clear()
        self.pointSrc.clear()
        self.zoneColor.clear()
        self.zones.clear()
        self.runable = False
        self.displayImage(self.image)
        self.laneAddBtn.show()
        self.laneRedoBtn.show()
        self.laneDeleteBtn.show()
        self.laneFinishBtn.show()
        # self.lanerestartBtn.show()
    def addFun(self):
        print(self.pointSrc,'self.pointSrc')
        print(np.array(self.pointSrc, np.int32), 'np.array')

        self.zones.append(np.array([self.pointSrc], np.int32))
        self.zoneColor.append(self.getRandomColor())
        self.pointSrc=[] 
        self.drawpolyline(self.image)

    def deleteFun(self):
       if(len(self.zones)>0):
            self.zones=self.zones[:-1]
            self.zoneColor=self.zoneColor[:-1]
            # print("remove last zone ",len(self.pointSrc))
            self.drawpolyline(self.image)

    def redoFun(self):
        if(len(self.pointSrc)>0):
            self.pointSrc = self.pointSrc[:-1]
            print("remove last ",len(self.pointSrc))
            self.drawpolyline(self.image)

    def saveFun(self, x, y):
        for i in range(len(self.zones)):
            bbPath = mplPath.Path(np.array(self.zones[i][0]))
            if bbPath.contains_point((x,y)):
                return i

    def loadvideo (self):
        self.runable = True
        counter=0
        ret = True
        self.laneAddBtn.hide()
        self.laneRedoBtn.hide()
        self.laneDeleteBtn.hide()
        self.laneFinishBtn.hide()
        # self.lanerestartBtn.hide()
        while(ret):
            if not self.runable:
                break
            ret, img = self.vidcap.read()
            img = cv2.resize(img,(1400,850))
            self.drawpolyline(img)
            QApplication.processEvents()


    def finsihFun(self):  
        self.df = pd.read_csv(self.csvpath, sep=',')
        self.userid = self.df[self.df['frameNUM']==2]
        # carinfo = self.userid[self.userid['carID']==2]
        # course = carinfo['course'].values[0]
        # print(carinfo)
        # print(course)

        carLanelist = []
        for i in range(len(self.userid)):
            cx = self.userid['carCenterX'].values[i]
            cy = self.userid['carCenterY'].values[i]
            print(int(cx/2.9), int(cy/2.5))
            lane = self.saveFun(int(cx/2.9), int(cy/2.5))
            print(lane)
            carLanelist.append([self.userid['carID'].values[i], lane])
        print(carLanelist)
        # carLanelist =[[0, 0], [1, None], [2, 0], [3, None], [4, 0], [5, 0], [6, 0], [7, 0], [8, None], [9, 0], [10, 2], [11, None], [12, 1], [13, None], [14, 1], [15, None], [16, None], [17, 2], [18, None], [19, None], [20, None], [21, None], [23, None]]
        optlist = []
        while len(carLanelist)>0:

            newfilter, carLanelist= self.filterCommon(carLanelist)
            optlist.append(newfilter)
        # print('=============output============')
        # print(optlist)
        frontcar = []
        for element in optlist:
            if element[0][1] is not None:
                print('=============element============')
                print(element)
                for i in range(len(element)):
                    if element[0][3] > element[i+1][3]:
                        print(element[i])

    def filterCommon(self, alist):
        filterlist = []
        listinfo = []
        fw = alist[0][1]

        for element in alist:
            # print(element,'element')

            if element[1] == fw:
                filterlist.append(element)

        if len(filterlist)>0:
            for element in filterlist:   
                alist.remove(element)
                carid = element[0]
                carinfo = self.userid[self.userid['carID']==carid]
                course = carinfo['course'].values[0]
                cx = carinfo['carCenterX'].values[0]
                cy = carinfo['carCenterY'].values[0]  
                listinfo.append([element[0], element[1], course, cx, cy])

        return listinfo, alist

    def drawpolyline(self, img):
        displayImg = img.copy()
        displayImg = self.displayPoint(displayImg, self.pointSrc,(255,255,0))
        for i in range(len(self.zones)):
    
            cv2.polylines(displayImg,[self.zones[i]],True,self.zoneColor[i],2)
            print(self.zones[i][0])
            print(self.zones[i][0][0])
            cv2.putText(displayImg, str(i), self.zones[i][0][0], self.font,0.6, (0,0,255), 1, cv2.LINE_AA)
            print('1121212')
        self.displayImage(displayImg)

    def displayPoint(self, displayImg, points,colors):
        font = cv2.FONT_HERSHEY_SIMPLEX 
        for i in range(len(self.pointSrc)):

            cv2.circle(displayImg,points[i],1,colors,1)
            cv2.putText(displayImg, str(i), points[i], font,0.4, colors, 1, cv2.LINE_AA)
        zoneDawing=np.array([self.pointSrc], np.int32).reshape((-1,1,2))
        cv2.polylines(displayImg,[zoneDawing],True,(0,255,0),2)
        return displayImg



    def displayImage(self, image):

        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg)
        self.lineSelectGV.scene().addPixmap(pix)


