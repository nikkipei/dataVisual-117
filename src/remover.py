from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import cv2
import cv2 as cv
import numpy as np
import random

class Remover(QWidget):
    def __init__(self, path, removeVideoParentswidget, removeGraphicsView, addBtn, redoBtn, deleteBtn, finishBtn, restartRMBtn,parent=None):
        super().__init__(parent)

        # self.path = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/sample5stab-10fpsstab.mp4'
        # vidcap = cv2.VideoCapture('/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/sample5stab-10fpsstab.mp4')
        vidcap = cv2.VideoCapture(path)
        self.videoWidth=vidcap.get(3)
        self.videoHeight=vidcap.get(4)
        self.videoFps=vidcap.get(5)

        success,image = vidcap.read()
        image = cv2.resize(image,(1200,800))

        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg)
        
        removeGraphicsView.setScene(QtWidgets.QGraphicsScene(self))
        removeGraphicsView.scene().addPixmap(pix)

        redoBtn.clicked.connect(self.redoFun)
        addBtn.clicked.connect(self.addFun)
        deleteBtn.clicked.connect(self.deleteFun)
        finishBtn.clicked.connect(self.finishFun)
        restartRMBtn.clicked.connect(self.restartFun)
        self.vidcap = vidcap
        self.removeGraphicsView = removeGraphicsView
        self.pointSrc=[]
        self.zoneColor=[]
        self.finishedInput=False

        self.pix = pix
        self.image = image
        self.font = cv2.FONT_HERSHEY_SIMPLEX 
        self.zones = []
        self.path = path
        # self.addBtn = addBtn
        # self.redoBtn = redoBtn
        # self.deleteBtn = deleteBtn
        # self.finishBtn = finishBtn
        # self.load(image)
        self.runable = True
    def restartFun(self):
        self.runable = False
        self.removeGraphicsView.scene().clear()
        self.removeGraphicsView.scene().addPixmap(self.pix)
        self.pointSrc.clear()
        self.zoneColor.clear()
        self.zones.clear()
        self.removeGraphicsView.scene().addPixmap(self.pix)

        # self.finishedInput=False

    def redoFun(self):
        if(len(self.pointSrc)>0):
            self.pointSrc = self.pointSrc[:-1]
            print("remove last ",len(self.pointSrc))
            self.displayImage(self.image)

    def addFun(self):
        self.zones.append(np.array([self.pointSrc], np.int32).reshape((-1,1,2)))
        self.zoneColor.append(self.getRandomColor())
        self.pointSrc=[] 
        self.displayImage(self.image)

    def deleteFun(self):
       if(len(self.zones)>0):
            self.zones=self.zones[:-1]
            self.zoneColor=self.zoneColor[:-1]
            print("remove last zone ",len(self.pointSrc))
            self.displayImage(self.image)

    def finishFun(self):
        self.runable = True
        scale=1
        counter=0
        ret = True
        # videoWidth=self.vidcap.get(3)
        # # print(videoWidth, 'videoWidth')
        # # print(self.image.width(),'self.image.width()')
        # videoHeight=self.vidcap.get(4)


        videoWidth = 1200
        videoHeight = 800
        videoFps=self.vidcap.get(5)

        ret, img = self.vidcap.read()
        print(ret)
        if(len(self.zones)>0):
            boundZone, zones= self.zones[0], self.zones[1:]
            np.save(self.path[:-4]+"BoundZone.npy",boundZone,allow_pickle=True)
            np.save(self.path[:-4]+"zones.npy",self.zones,allow_pickle=True)
            blank_image = np.zeros((round(videoHeight*scale),round(videoWidth*scale),3), np.uint8)
            for zone in self.zones:
            # maskZone=[(405,340),(459,317),(471,338),(421,369)]
                maskZone = np.array(zone, np.int32).reshape((-1,1,2))
                blank_image=cv2.fillPoly(blank_image,[maskZone],(255,255,255))


            grey_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
            grey_image = np.uint8(grey_image)

            vid_writer = cv2.VideoWriter(self.path[:-4]+"final.avi", cv2.VideoWriter_fourcc('M','J','P','G'), videoFps, (round(videoWidth),round(videoHeight)))
            videoName = self.path[:-4]+"final.avi"
            backSub = cv2.createBackgroundSubtractorMOG2()
            cap = cv.VideoCapture(self.path)
            counter=0
            while(ret):
              # 读取视频
                if not self.runable:
                    break

                ret, img = cap.read()
                if img is None:
                    break
                img = cv2.resize(img,(1200,800))
                frame=img.copy()
                frame = cv2.bitwise_and(frame, frame, mask=grey_image)
                blur = cv.blur(frame,(15,15))
                inpaint = cv2.inpaint(img,grey_image,3,cv2.INPAINT_TELEA)
                fgMask = backSub.apply(blur)
                ret,thresh1 = cv.threshold(fgMask,200,255,cv.THRESH_BINARY)
                blank_image_r=cv2.bitwise_not(blank_image)
                grey_image_r = cv2.cvtColor(blank_image_r, cv2.COLOR_BGR2GRAY)
                replaced_image = cv2.bitwise_and(img,img,mask = grey_image_r)
                car = cv2.bitwise_or(img, img, mask=thresh1)
                th_r=cv2.bitwise_not(thresh1)
                inpaintCrop= cv2.bitwise_and(inpaint, inpaint, mask=th_r)
                dst = cv2.addWeighted(car,1,inpaintCrop,1,0)

                b,g,r = cv2.split(dst)           # get b, g, r
                rgb_img1 = cv2.merge([r,g,b])

                height, width, channel = rgb_img1.shape
                bytesPerLine = 3 * width
                qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pix = QPixmap(qImg)
                self.removeGraphicsView.scene().clear()
                self.removeGraphicsView.scene().addPixmap(pix)
                QApplication.processEvents()
                print(self.removeGraphicsView.scene().items())
                print(str(counter)+"/"+str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
                counter+=1
                vid_writer.write(dst.astype(np.uint8))

        print('finished')
        msg = 'Completed! Video has saved in: ' +videoName +"'"
        QMessageBox.about(self, "Completed", msg)
        self.restartFun()
    def getRandomColor(self):
        return (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.removeGraphicsView.mapToScene(event.pos())
            item = self.removeGraphicsView.scene().itemAt(QPointF(scene_pos), QTransform())
            if type(item) is QGraphicsPixmapItem:
                
                mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())

                if(self.finishedInput and len(pointInput)<=len(self.pointSrc)):
                    print("canot add")
                else:
                    tmpColor=self.getRandomColor()
                    #colorSrc.append(tmpColor)
                    self.pointSrc.append((mouseX,mouseY))

                    # displayImg = self.image.copy()
                    # displayImg = self.displayPoint(displayImg, self.pointSrc,(255,255,0))
                    # cv2.putText(displayImg, "you are drawing zone:"+str(len(self.zones)), (100,50), self.font,1, (0,0,255), 2, cv2.LINE_AA)
                    self.displayImage(self.image)

                    print(self.pointSrc)
                    print("added ")


    def displayImage(self, img):
        self.removeGraphicsView.scene().clear()
        displayImg = img.copy()
        displayImg = self.displayPoint(displayImg, self.pointSrc,(255,255,0))

        cv2.putText(displayImg, "you are drawing zone:"+str(len(self.zones)), (50,50), self.font, 0.6, (255,255,0), 1, cv2.LINE_AA)

        for i in range(len(self.zones)):
    
            cv2.polylines(displayImg,[self.zones[i]],True,self.zoneColor[i],2)


        b,g,r = cv2.split(displayImg)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg)
        self.removeGraphicsView.scene().addPixmap(pix)
        print(self.removeGraphicsView.scene().items())
        # self.redoBtn.clicked.connect(self.redoFun)

    def displayPoint(self, displayImg,points,colors):
        font = cv2.FONT_HERSHEY_SIMPLEX 
        for i in range(len(self.pointSrc)):

            cv2.circle(displayImg,points[i],1,colors,1)
            cv2.putText(displayImg, str(i), points[i], font,0.4, colors, 1, cv2.LINE_AA)
        zoneDawing=np.array([self.pointSrc], np.int32).reshape((-1,1,2))
        cv2.polylines(displayImg,[zoneDawing],True,(0,255,0),2)
        return displayImg
