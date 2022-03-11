from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import cv2, imutils
import time
import numpy as np
# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
import numpy as np
import cv2
# import pyshine as ps
#problem video not save
class Stabilization(QWidget):
    def __init__(self, path, videoStable, stabLoadVideobtn, graphicsViewStab, restartBtn, parent=None):
        super().__init__(parent)

        restartBtn.clicked.connect(self.restartFunc)

        stabLoadVideobtn.clicked.connect(self.btnClick)
        stabLoadVideobtn.setEnabled(False)
        self.stabLoadVideobtn = stabLoadVideobtn

        vidcap = cv2.VideoCapture(path)
        success,image = vidcap.read()
        image = cv2.resize(image,(graphicsViewStab.width()-20,graphicsViewStab.height()-20))
        count = 0

        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        # print(success,"zai html limian de image")
        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg)
        # pix = pix.scaled(graphicsViewStab.width(),graphicsViewStab.height())
        # print(graphicsViewStab.width(), graphicsViewStab.height())
        # video_pixmap = QGraphicsPixmapItem(pix)
        # video_pixmap.setZValue(-100)
        # video_pixmap.setPos(1, 1)

        graphicsViewStab.setScene(QtWidgets.QGraphicsScene(self))
        self.itemPix = graphicsViewStab.scene().addPixmap(pix)

        print(graphicsViewStab.scene().items(), 'items in first')
        # graphicsViewStab.scene().addItem(video_pixmap)

        # graphicsViewStab.setFocusPolicy(Qt.StrongFocus)
        # graphicsViewStab.setFocus()

        # self.scene  = QGraphicsScene()
        # self.scene.addPixmap(pix)
        # graphicsViewStab = QGraphicsView(self.scene, self)
        self.m_rubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle
        )
        self.m_rubberBand.setGeometry(QtCore.QRect(-1, -1, 2, 2))
        self.m_rubberBand.hide()
        self.m_rubberBand.setWindowOpacity(0.5)
        self.rubberitem = graphicsViewStab.scene().addWidget(self.m_rubberBand)
        self.rubberitem.setZValue(1)
        self.m_draggable = False
        self.m_origin = QtCore.QPoint()



        self.redBrush = QBrush(Qt.red)
        self.pen = QPen(Qt.blue)

        self.graphicsViewStab = graphicsViewStab
        self.pix = pix
        self.path = path
        self.vidcap =vidcap
        self.videoStable = videoStable
        self.bbox = []
        self.image = image
        self.trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        # self.load(image)
        # self.scene = scene
        # self.view = view
        self.pts1 = 0
        self.restartBtn = restartBtn

        self.runable = True
        self.rect = []

    def load(self, frame):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        outputfile = self.path[:-4]+"stab.mp4"
        # print(outputfile)
        rows,cols = frame.shape[:2]
        inputWidth=cols
        inputHeight=rows
        videoFPS= self.vidcap.get(cv2.CAP_PROP_FPS)
        # vid_writer = cv2.VideoWriter(outputfile, cv2.VideoWriter_fourcc('M','P','4','V'), videoFPS, (round(inputWidth),round(inputHeight)))
        vid_writer = cv2.VideoWriter(outputfile, fourcc, videoFPS, (round(inputWidth),round(inputHeight)))

        trackerType = "CSRT"
        trackers,initPoints=self.createLandMarker(6,frame,trackerType,1)
        self.pts1 = np.float32(initPoints)
        # print('finsihing loading')
        cap = cv2.VideoCapture(self.path)
        counter=0
        while True:
            if not self.runable:
                break
                # Read a new frame
            ok, frame2 = cap.read()
            frame2 = cv2.resize(frame2,(self.graphicsViewStab.width()-20,self.graphicsViewStab.height()-20))

            if not ok:
                 break
                # Start timer
            timer = cv2.getTickCount()
                # Update tracker
            tmpTrackers=trackers
            if(counter%5==0 or counter==0):
                Matrix=self.fixVideo(tmpTrackers,frame2)
            frame2 = cv2.warpPerspective(frame2,Matrix,(cols,rows))
                    # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
            print(str(counter)+"/"+str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
            vid_writer.write(frame2.astype(np.uint8))
            b,g,r = cv2.split(frame2)
            rgb_img1 = cv2.merge([r,g,b])
            height, width, channel = rgb_img1.shape      

            bytesPerLine = 3 * width
            qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap(qImg)
            # video_pixmap = QGraphicsPixmapItem(pix)
            # self.graphicsViewStab.scene().addItem(frame2)
            self.graphicsViewStab.scene().addPixmap(pix)
            QApplication.processEvents()
            # cv2.imshow("Tracking", frame)
            print('finsihing one frame')
            counter+=1
            # self.graphicsViewStab.scene.removeItem(self.graphicsViewStab.scene.items()[0])

        msg = 'Completed! Video has saved in ' +outputfile +"'"
        QMessageBox.about(self, "Completed", msg)
        self.restartFunc()


    def restartFunc(self):
        # print(self.graphicsViewStab.scene().items())
        # print(self.graphicsViewStab.scene().Rect(),'rectangle')
        # self.graphicsViewStab.scene().addPixmap(self.pix)
        self.runable = False
        # for i in range(0,len(self.rect)):
        #     self.graphicsViewStab.scene().removeItem(self.rect[i])

        # self.graphicsViewStab.scene().addPixmap(self.pix)
        # self.graphicsViewStab.scene().removeItem(self.prePix)
        for item in self.graphicsViewStab.scene().items():
            if item != self.rubberitem and item != self.itemPix:
                self.graphicsViewStab.scene().removeItem(item)

        # self.graphicsViewStab.scene().addPixmap(self.pix)
        self.bbox.clear()
        # print(self.graphicsViewStab.scene().items(),'restart items')
        # print(self.bbox)
    def fixVideo(self, trackers,frame):
        # Draw bounding box
        # rows,cols = frame.shape[:2]
        newCenterPoints=[]
        for i in range(len(trackers)):
            # print('ok in fixvideo: ', ok)
            # print('trackers[i].update(frame): ', trackers[i].update(frame))
            ok, bbox = trackers[i].update(frame)
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            cv2.circle(frame, (int(bbox[0] + bbox[2]/2),int(bbox[1] + bbox[3]/2)), 5, (0,255,0), 3)
            newCenterPoints.append((int(bbox[0] + bbox[2]/2),int(bbox[1] + bbox[3]/2)))
        pts2 = np.float32(newCenterPoints)
        #M = cv2.getPerspectiveTransform(pts2,pts1)xs
        M, status = cv2.findHomography(pts2, self.pts1)
        #dst = cv2.warpPerspective(frame,M,(cols,rows))
        return M
    def createTrackerByName(self, trackerType):
      # Create a tracker based on tracker name
        if trackerType == self.trackerTypes[0]:
            tracker = cv2.TrackerBoosting_create()
        elif trackerType == self.trackerTypes[1]: 
            tracker = cv2.TrackerMIL_create()
        elif trackerType == self.trackerTypes[2]:
            tracker = cv2.TrackerKCF_create()
        elif trackerType == self.trackerTypes[3]:
            tracker = cv2.TrackerTLD_create()
        elif trackerType == self.trackerTypes[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif trackerType == self.trackerTypes[5]:
            tracker = cv2.TrackerGOTURN_create()
        elif trackerType == self.trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == self.trackerTypes[7]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in self.trackerTypes:
                print(t)
        return tracker

    def createLandMarker(self, number,frame,Type,rate):
        frameRize = cv2.resize(frame,None,fx=rate,fy=rate)   
        tmpTrackers=[]
        tmpCenterPoints=[]
        for i in range(number):
            tmpCenterPoints.append((self.bbox[i][4], self.bbox[i][5]))
            tmpBbox = (int(self.bbox[i][0]), int(self.bbox[i][1]),
                int(self.bbox[i][2]), int(self.bbox[i][3]))

            tmpTrackers.append(self.createTrackerByName(Type))
            ok = tmpTrackers[i].init(frame, tmpBbox)

        return tmpTrackers,tmpCenterPoints     

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.graphicsViewStab.mapToScene(event.pos())

            item = self.graphicsViewStab.scene().itemAt(QPointF(scene_pos), QTransform())

            if type(item) is QGraphicsPixmapItem:
                # print()
                self.m_origin = self.graphicsViewStab.mapToScene(event.pos()).toPoint()
                # print(self.m_origin)
                self.m_rubberBand.setGeometry(
                    QtCore.QRect(self.m_origin, QtCore.QSize())
                )

                self.m_rubberBand.show()
                self.m_draggable = True
            # self.m_draggable = True
            # print(self.m_draggable)
            # super(Stabilization, self).mousePressEvent(event)
            # print(event.pos())
    def mouseMoveEvent(self, event):
        # scene_pos = self.graphicsViewStab.mapToScene(event.pos())

        # item = self.graphicsViewStab.scene().itemAt(QPointF(scene_pos), QTransform())

        # if type(item) is QGraphicsPixmapItem:
        if self.m_draggable:
            end_pos = self.graphicsViewStab.mapToScene(event.pos()).toPoint()
            self.m_rubberBand.setGeometry(
                QtCore.QRect(self.m_origin, end_pos).normalized()
            )
            self.m_rubberBand.show()
            self.stabLoadVideobtn.setEnabled(True)
            # print('move')
    def mouseReleaseEvent(self, event):
        # scene_pos = self.graphicsViewStab.mapToScene(event.pos())

        # item = self.graphicsViewStab.scene().itemAt(QPointF(scene_pos), QTransform())

        # if type(item) is QGraphicsPixmapItem:
        end_pos = self.graphicsViewStab.mapToScene(event.pos()).toPoint()
        self.m_rubberBand.setGeometry(
            QtCore.QRect(self.m_origin, end_pos).normalized()
        )
        rec = QtCore.QRect(self.m_origin, end_pos).normalized()
        # print(QtCore.QRect(self.m_origin, end_pos).normalized())
        # print(QtCore.QRect(self.m_origin, end_pos).normalized().width())

        # self.shapes(rec.x(), rec.y(), rec.width(), rec.height() )
        # print(rec.x(), rec.y(), rec.width(), rec.height() ,"rect size")
        self.m_draggable = False


    def shapes(self, x, y, w, h):
            # ellipse = self.scene.addEllipse(20,20, 200,200, self.pen, self.greenBrush)
           
            rectangle = self.graphicsViewStab.scene().addRect(x, y, w, h, self.pen)
            
            self.rect.append(rectangle)
            centerx = int(x/1 + w/2/1)
            centery = int(y/1 + h/2/1)
            ellipse = self.graphicsViewStab.scene().addEllipse(centerx, centery, 5,5, self.pen, self.redBrush)
            

            rectangle.setZValue(100)
            self.rect.append(ellipse)

            self.bbox.append([x, y, w, h, centerx, centery])
            self.stabLoadVideobtn.setEnabled(False)
            if len(self.bbox) == 6:
                self.runable = True
                print(self.graphicsViewStab.scene().items(), 'self.graphicsViewStab.scene()')
                print(self.bbox)
                self.load(self.image)

    def btnClick(self):
        # print('click')
        self.shapes(self.m_rubberBand.x(), self.m_rubberBand.y(), self.m_rubberBand.width(), 
            self.m_rubberBand.height())
        self.m_rubberBand.hide()
        

