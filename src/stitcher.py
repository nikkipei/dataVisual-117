from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from skimage import exposure

class Stitcher(QWidget):
    def __init__(self,stitchgraphicsView, prevBtn1, nextBtn1,stitchgraphicsView2, 
                prevBtn2, nextBtn2, stitchgraphicsView3, prevBtn3, nextBtn3, 
                leftBtn, midBtn, rightBtn, loadBtn, leftEdit, midEdit, rightEdit, 
                horizontalSlider2, stitlLabel1, horizontalSlider1, stitlLabel2, 
                horizontalSlider3, stitlLabel3, graphicsView_2,  matchColorChecked1,
                matchColorChecked2, matchColorChecked3, redo1btn, redo2btn, redo4btn, redo3btn, 
                previewBtn, startBtn, backBtn, parent=None):

        super().__init__(parent)

        # # self.path

        # print(path, 'path')
        # path = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/Drone A-1-004stabout.mp4'
        # vidcap = cv2.VideoCapture(path)

        # success,image = vidcap.read()
        # # np.triu((1, size, size), k=1).astype("uint8")
        # # image = np.zeros((500,500, 3))*250s
        # # image[:,0:500//2] = (19,19,19)
        # # image.fill(250)
        # b,g,r = cv2.split(image)           # get b, g, r
        # rgb_img1 = cv2.merge([r,g,b])

        # height, width, channel = rgb_img1.shape
        # bytesPerLine = 3 * width
        # qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # pix = QPixmap(qImg)


        # stitchgraphicsView.setScene(QtWidgets.QGraphicsScene(self))
        # stitchgraphicsView.scene().addPixmap(pix)
        # path = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/Drone A-2-004stabout.mp4'
        # path2 = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/Drone B-1-002stabout.mp4'
        # path3 = '/Users/nikkipei/Documents/Projects/ATTAIN3/data/video/Drone C-1-001stabout.mp4'
        # vidcap = cv2.VideoCapture(path)
        # vidcap2 = cv2.VideoCapture(path2)
        # vidcap3 = cv2.VideoCapture(path3)

        horizontalSlider1.hide()
        stitlLabel1.hide()
        prevBtn1.hide()
        nextBtn1.hide() 
        horizontalSlider2.hide()
        stitlLabel2.hide()
        prevBtn2.hide()
        nextBtn2.hide() 
        horizontalSlider3.hide()
        stitlLabel3.hide()
        prevBtn3.hide()
        nextBtn3.hide() 
        graphicsView_2.hide()
        matchColorChecked1.hide()
        matchColorChecked2.hide()
        matchColorChecked3.hide()

        redo1btn.hide()
        redo2btn.hide()
        redo4btn.hide()
        redo3btn.hide() 
        previewBtn.hide()
        previewBtn.clicked.connect(self.findHomograFun)

        startBtn.hide()
        startBtn.clicked.connect(self.processNewVideo)

        backBtn.hide()
        backBtn.clicked.connect(self.loadFun)

        leftBtn.setEnabled(True)
        leftBtn.clicked.connect(self.leftFun)

        midBtn.setEnabled(True)
        midBtn.clicked.connect(self.midFun)

        rightBtn.setEnabled(True)
        rightBtn.clicked.connect(self.rightFun)
        # rightBtn.clicked.connect(self.findHomograFun)
        loadBtn.setEnabled(True)
        loadBtn.clicked.connect(self.loadFun)

        stitchgraphicsView.setScene(QtWidgets.QGraphicsScene(self))
        stitchgraphicsView2.setScene(QtWidgets.QGraphicsScene(self))
        stitchgraphicsView3.setScene(QtWidgets.QGraphicsScene(self))
        graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))

        # self.leftBtn = leftBtn
        # self.midBtn = midBtn
        # self.rightBtn = rightBtn
        # self.leftBtn = leftBtn
        # self.leftBtn = leftBtn
        # self.leftBtn = leftBtn
        # self.leftBtn = leftBtn


        self.stitchgraphicsView = stitchgraphicsView
        self.horizontalSlider1 = horizontalSlider1
        self.stitlLabel1 = stitlLabel1
        self.prevBtn1 = prevBtn1
        self.nextBtn1 = nextBtn1

        self.horizontalSlider2 = horizontalSlider2
        self.stitlLabel2 = stitlLabel2
        self.prevBtn2 = prevBtn2
        self.nextBtn2 = nextBtn2
        self.stitchgraphicsView2 = stitchgraphicsView2

        self.horizontalSlider3 = horizontalSlider3
        self.stitlLabel3= stitlLabel3
        self.prevBtn3 = prevBtn3
        self.nextBtn3 = nextBtn3
        self.stitchgraphicsView3 = stitchgraphicsView3
          
        self.loadBtn = loadBtn
        self.leftBtn = leftBtn
        self.midBtn = midBtn
        self.rightBtn = rightBtn

        self.leftEdit = leftEdit
        self.midEdit = midEdit
        self.rightEdit = rightEdit

        # self.vidcap = ''
        # self.vidcap2 = ''
        # self.vidcap3 = ''

        self.matchColorChecked1 = matchColorChecked1
        self.matchColorChecked2 = matchColorChecked2
        self.matchColorChecked3 = matchColorChecked3

        self.redo1btn = redo1btn
        self.redo2btn = redo2btn
        self.redo4btn = redo4btn
        self.redo3btn = redo3btn
        self.previewBtn = previewBtn
        self.startBtn = startBtn
        self.backBtn = backBtn

        self.stitchgraphicsView.viewport().installEventFilter(self)
        self.stitchgraphicsView2.viewport().installEventFilter(self)
        self.stitchgraphicsView3.viewport().installEventFilter(self)
        self.graphicsView_2 = graphicsView_2
        self.path=[]
        self.pointSrc1=[]
        self.pointSrc2=[]
        self.pointSrc2display=[]
        self.pointSrc3=[]
        self.pointSrc4=[]
        self.runable = True
        # self.H =
        # self.images = []
        self.current_item = None
        self.start_pos = QPointF()
        self.end_pos = QPointF()

        self.redo1btn.clicked.connect(lambda:self.redo(self.horizontalSlider1,self.vidcap, self.stitchgraphicsView, self.pointSrc1))
        self.redo2btn.clicked.connect(lambda:self.redo2(self.horizontalSlider2,self.vidcap2, self.stitchgraphicsView2, self.pointSrc2))
        self.redo3btn.clicked.connect(lambda:self.redo(self.horizontalSlider3,self.vidcap3, self.stitchgraphicsView3, self.pointSrc3))
        self.redo4btn.clicked.connect(lambda:self.redo2(self.horizontalSlider2,self.vidcap2, self.stitchgraphicsView2, self.pointSrc4))

        self.prevBtn1.clicked.connect(lambda: self.preFrame(self.vidcap, self.horizontalSlider1, self.stitchgraphicsView, self.stitlLabel1, self.pointSrc1))
        self.nextBtn1.clicked.connect(lambda: self.nextFrame(self.vidcap, self.horizontalSlider1, self.stitchgraphicsView, self.stitlLabel1, self.pointSrc1))
        self.horizontalSlider1.valueChanged.connect(lambda: self.changed_slider1(self.vidcap, self.horizontalSlider1, self.stitchgraphicsView, self.stitlLabel1, self.pointSrc1))

        self.prevBtn2.clicked.connect(lambda: self.preFrame(self.vidcap2, self.horizontalSlider2, self.stitchgraphicsView2, self.stitlLabel2, self.pointSrc2))
        self.nextBtn2.clicked.connect(lambda: self.nextFrame(self.vidcap2, self.horizontalSlider2, self.stitchgraphicsView2, self.stitlLabel2, self.pointSrc2))
        self.horizontalSlider2.valueChanged.connect(lambda: self.changed_slider1(self.vidcap2, self.horizontalSlider2, self.stitchgraphicsView2, self.stitlLabel2, self.pointSrc2))

        self.prevBtn3.clicked.connect(lambda: self.preFrame(self.vidcap3, self.horizontalSlider3, self.stitchgraphicsView3, self.stitlLabel3, self.pointSrc3))
        self.nextBtn3.clicked.connect(lambda: self.nextFrame(self.vidcap3, self.horizontalSlider3, self.stitchgraphicsView3, self.stitlLabel3, self.pointSrc3))
        self.horizontalSlider3.valueChanged.connect(lambda: self.changed_slider1(self.vidcap3, self.horizontalSlider3, self.stitchgraphicsView3, self.stitlLabel3,self.pointSrc3))
        

    def loadFun(self):
        self.runable = False
        self.vidcap = cv2.VideoCapture(self.path[0])
        self.vidcap2 = cv2.VideoCapture(self.path[1])
        self.vidcap3 = cv2.VideoCapture(self.path[2])
        #set frame number jump
        frameTotal = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        frameTotal2 = self.vidcap2.get(cv2.CAP_PROP_FRAME_COUNT)
        frameTotal3 = self.vidcap3.get(cv2.CAP_PROP_FRAME_COUNT)
        print(frameTotal,frameTotal2, frameTotal3)

        self.loadFrame(0, self.vidcap, self.stitchgraphicsView)
        self.loadFrame(0, self.vidcap2, self.stitchgraphicsView2)
        self.loadFrame(0, self.vidcap3, self.stitchgraphicsView3)
        self.matchColorChecked1.show()
        self.matchColorChecked2.show()
        self.matchColorChecked3.show()
        self.horizontalSlider1.show()
        self.stitlLabel1.show()

        self.horizontalSlider2.show()
        self.stitlLabel2.show()
        self.prevBtn2.show()
        self.nextBtn2.show() 
        self.horizontalSlider3.show()
        self.stitlLabel3.show()
        self.prevBtn3.show()
        self.nextBtn3.show() 

        self.prevBtn1.show()
        self.nextBtn1.show()

        self.redo1btn.show()
        self.redo2btn.show()
        self.redo4btn.show()
        self.redo3btn.show()
        self.previewBtn.show()
        self.loadBtn.show()
        self.leftBtn.show()
        self.midBtn.show()
        self.rightBtn.show()

        self.leftEdit.show()
        self.midEdit.show()
        self.rightEdit.show()
        self.stitchgraphicsView.show()
        self.stitchgraphicsView2.show()
        self.stitchgraphicsView3.show()

        self.startBtn.hide()
        self.backBtn.hide()
        self.graphicsView_2.hide()

        self.horizontalSlider1.setMaximum(frameTotal-1)
        self.horizontalSlider2.setMaximum(frameTotal2-1)
        self.horizontalSlider3.setMaximum(frameTotal3-1)

        # self.horizontalSlider1.setValue(0)
        # self.horizontalSlider2.setValue(0)
        # self.horizontalSlider3.setValue(0)
        self.displayImage(self.horizontalSlider1.value(), self.vidcap, self.stitchgraphicsView, self.pointSrc1)
        self.displayImage2(self.horizontalSlider2.value(), self.vidcap2, self.stitchgraphicsView2, self.pointSrc2)        
        self.displayImage(self.horizontalSlider3.value(), self.vidcap3, self.stitchgraphicsView3, self.pointSrc3)
        self.frameTotal = frameTotal
        self.lastFrame1 = 0
    
    def redo(self, horizontalSlider, vidcap, stitchgraphicsView, pointSrc):
        if pointSrc:
            pointSrc.pop()
            self.displayImage(horizontalSlider.value(), vidcap, stitchgraphicsView, pointSrc)

    def redo2(self, horizontalSlider, vidcap, stitchgraphicsView, pointSrc):
        if pointSrc:
            pointSrc.pop()
            self.displayImage2(horizontalSlider.value(), vidcap, stitchgraphicsView, pointSrc)

    def warpImages(self, img1, img2, H):

        rows1, cols1 = img1.shape[:2]
        rows2, cols2 = img2.shape[:2]

        list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
        temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)

        # When we have established a homography we need to warp perspective
        # Change field of view
        list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

        list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

        [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

        translation_dist = [-x_min,-y_min]

        H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

        output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
        print((x_max-x_min, y_max-y_min),'(x_max-x_min, y_max-y_min)')
        output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

        return output_img

    def processNewVideo(self):
        self.runable = True
        # self.startBtn.hide()
        # self.backBtn.hide()
        self.graphicsView_2.scene().clear()
        scale=1
        counter=0
        ret = True
        videoWidth = 1200
        videoHeight = 800
        videoFps=self.vidcap.get(5)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        vid_writer = cv2.VideoWriter(self.path[0][:-4]+"stitched.mp4", fourcc, videoFps, (round(videoWidth),round(videoHeight)))
        print(self.M)

        while(ret):
            if not self.runable:
                    break
            success,img1 = self.vidcap.read()

            success,img2 = self.vidcap2.read()

            success,img3 = self.vidcap3.read()

            if img1 is None:
                    break
            if img2 is None:
                    break
            if img3 is None:
                    break
            if self.matchColorChecked1.isChecked():
                img1 = exposure.match_histograms(img1, img3, multichannel=True)
            if self.matchColorChecked2.isChecked():
                img2 = exposure.match_histograms(img2, img1, multichannel=True)
            if self.matchColorChecked3.isChecked():
                img3 = exposure.match_histograms(img3, img1, multichannel=True)

            dim = (520, 350)
            img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
            img2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
            img3 = cv2.resize(img3, dim, interpolation = cv2.INTER_AREA)  


            print(1)
            result = self.warpImages( img2, img1, self.M)
            result2 = self.warpImages( img3, result, self.M2)
            
            b,g,r = cv2.split(result2)           # get b, g, r
            rgb_img1 = cv2.merge([r,g,b])
            height, width, channel = rgb_img1.shape
            bytesPerLine = 3 * width
            qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap(qImg)
            self.graphicsView_2.scene().clear()   
            self.graphicsView_2.scene().addPixmap(pix)
            QApplication.processEvents()
            print(self.graphicsView_2.scene().items())
            vid_writer.write(result2.astype(np.uint8))
            print(str(counter)+"/"+str(int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))))
            counter+=1
        print('finished')

    # def matchingColor(self):
    #     self.matchColorChecked1.hide()
    #     self.matchColorChecked2.hide()
    #     self.matchColorChecked3.hide()
    #     self.horizontalSlider1.hide()
    #     self.stitlLabel1.hide()
    #     self.prevBtn1.hide()
    #     self.nextBtn1.hide() 
    #     self.horizontalSlider2.hide()
    #     self.stitlLabel2.hide()
    #     self.prevBtn2.hide()
    #     self.nextBtn2.hide() 
    #     self.horizontalSlider3.hide()
    #     self.stitlLabel3.hide()
    #     self.prevBtn3.hide()
    #     self.nextBtn3.hide() 
    #     self.stitchgraphicsView.hide()
    #     self.stitchgraphicsView2.hide()
    #     self.stitchgraphicsView3.hide()

    #     self.graphicsView_2.show()

    #     # scale=1
    #     # counter=0
    #     # ret = True
    #     # videoWidth = 1200
    #     # videoHeight = 800
    #     # videoFps=self.vidcap.get(5)
    #     # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    #     # vid_writer = cv2.VideoWriter(self.path[:-4]+"matched.mp4", fourcc, videoFps, (round(videoWidth),round(videoHeight)))
        
    #     success,img1 = self.vidcap.read()
    #     success,img2 = self.vidcap2.read()

    #     matched = exposure.match_histograms(img2, img1, multichannel=True)

    #     # dim = (520, 350)
    #     # img2 = cv2.resize(matched, dim, interpolation = cv2.INTER_AREA)

    #     b,g,r = cv2.split(matched)           # get b, g, r
    #     rgb_img1 = cv2.merge([r,g,b])
    #     height, width, channel = rgb_img1.shape
    #     bytesPerLine = 3 * width
    #     qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #     pix = QPixmap(qImg)

    #     self.graphicsView_2.scene().addPixmap(pix)

    def findHomograFun(self):
        self.startBtn.show()
        self.backBtn.show()
        self.matchColorChecked1.hide()
        self.matchColorChecked2.hide()
        self.matchColorChecked3.hide()
        self.horizontalSlider1.hide()
        self.stitlLabel1.hide()
        self.prevBtn1.hide()
        self.nextBtn1.hide() 
        self.horizontalSlider2.hide()
        self.stitlLabel2.hide()
        self.prevBtn2.hide()
        self.nextBtn2.hide() 
        self.horizontalSlider3.hide()
        self.stitlLabel3.hide()
        self.prevBtn3.hide()
        self.nextBtn3.hide() 
        self.stitchgraphicsView.hide()
        self.stitchgraphicsView2.hide()
        self.stitchgraphicsView3.hide()
        self.redo1btn.hide()
        self.redo2btn.hide()
        self.redo4btn.hide()
        self.redo3btn.hide()
        self.previewBtn.hide()
        self.loadBtn.hide()
        self.leftBtn.hide()
        self.midBtn.hide()
        self.rightBtn.hide()

        self.leftEdit.hide()
        self.midEdit.hide()
        self.rightEdit.hide()

        self.graphicsView_2.show()

        dx = (self.pointSrc1[0][0]) - (self.pointSrc2[0][0])
        dy = (self.pointSrc1[0][1]) - (self.pointSrc2[0][1])

        self.pointSrc2.clear()
        for item in (self.pointSrc1):
            x = item[0]-dx
            y = item[1]-(dy)
            self.pointSrc2.append((x,y))

        dx2 = (self.pointSrc4[0][0]) - (self.pointSrc3[0][0])
        dy2 = (self.pointSrc4[0][1]) - (self.pointSrc3[0][1])
        print(dx2,dy2,'xy2')
        self.pointSrc3.clear()
        for item in (self.pointSrc4):
            x = item[0]-dx2
            y = item[1]-(dy2)
            self.pointSrc3.append((x,y))

        # self.pointSrc4.clear()
        self.pointSrc4new = []
        for item in (self.pointSrc4):
            x = item[0]+dx
            self.pointSrc4new.append((x, item[1]))

        

        src1 = np.float32(self.pointSrc1).reshape(-1,1,2)
        src2 = np.float32(self.pointSrc2).reshape(-1,1,2)

        src3 = np.float32(self.pointSrc3).reshape(-1,1,2)
        src4 = np.float32(self.pointSrc4new).reshape(-1,1,2)
       
        self.M, _ = cv2.findHomography(src1, src2, cv2.RANSAC, 5.0)
        self.M2, _ = cv2.findHomography(src4, src3, cv2.RANSAC, 5.0)

        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, self.horizontalSlider1.value())
        success,img1 = self.vidcap.read()

        self.vidcap2.set(cv2.CAP_PROP_POS_FRAMES, self.horizontalSlider2.value())
        success,img2 = self.vidcap2.read()

        self.vidcap3.set(cv2.CAP_PROP_POS_FRAMES, self.horizontalSlider3.value())
        success,img3 = self.vidcap3.read()
        if self.matchColorChecked1.isChecked():
            img1 = exposure.match_histograms(img1, img3, multichannel=True)
        if self.matchColorChecked2.isChecked():
            img2 = exposure.match_histograms(img2, img1, multichannel=True)
        if self.matchColorChecked3.isChecked():
            img3 = exposure.match_histograms(img3, img1, multichannel=True)

        dim = (520, 350)

        img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
        img2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
        img3 = cv2.resize(img3, dim, interpolation = cv2.INTER_AREA)
        # width = trainImg.shape[1] + queryImg.shape[1]
        # height = trainImg.shape[0] + queryImg.shape[0]

        # result = cv2.warpPerspective(trainImg, M, (width, height))
        # result[0:queryImg.shape[0], 0:queryImg.shape[1]] = queryImg

        result = self.warpImages( img2, img1, self.M)
        result2 = self.warpImages( img3, result, self.M2)
        # cv2_imshow(result)
        # result = cv2.resize(result, (800,400), interpolation = cv2.INTER_AREA)
        b,g,r = cv2.split(result2)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 

        self.graphicsView_2.scene().addPixmap(pix)

    def eventFilter(self, o, e):
        if self.stitchgraphicsView.viewport() is o:
            if e.type() == QEvent.MouseButtonPress:
                if e.buttons() & Qt.LeftButton:
                    print("press1")
                    scene_pos = self.stitchgraphicsView.mapToScene(e.pos())
                    item = self.stitchgraphicsView.scene().itemAt(QPointF(scene_pos), QTransform())
                    if type(item) is QGraphicsPixmapItem:
                        print('pressed in map')
                        mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                        print(mouseX, mouseY)
                        self.pointSrc1.append((mouseX,mouseY))
                        self.displayImage(self.horizontalSlider1.value(), self.vidcap, self.stitchgraphicsView, self.pointSrc1)
                        # print(self.pointSrc1)
                        print("added ")

        if self.stitchgraphicsView2.viewport() is o:
            if e.type() == QEvent.MouseButtonPress:
                if e.buttons() & Qt.LeftButton:
                    print("press2")
                    scene_pos = self.stitchgraphicsView2.mapToScene(e.pos())
                    item = self.stitchgraphicsView2.scene().itemAt(QPointF(scene_pos), QTransform())
                    if type(item) is QGraphicsPixmapItem:
                        mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                        if mouseX < 250:
                            print(mouseX, mouseY)
                            self.pointSrc2.append((mouseX,mouseY))
                            self.pointSrc2display.append(((mouseX,mouseY)))
                            self.displayImage2(self.horizontalSlider2.value(), self.vidcap2, self.stitchgraphicsView2, self.pointSrc2)
                            # print(self.pointSrc2)
                            print("added")
                        else:
                            self.pointSrc2display.append(((mouseX,mouseY)))
                            self.pointSrc4.append((mouseX,mouseY))
                            self.displayImage2(self.horizontalSlider2.value(), self.vidcap2, self.stitchgraphicsView2, self.pointSrc4)
                            print()

        if self.stitchgraphicsView3.viewport() is o:
            if e.type() == QEvent.MouseButtonPress:
                if e.buttons() & Qt.LeftButton:
                    print("press2")
                    scene_pos = self.stitchgraphicsView3.mapToScene(e.pos())
                    item = self.stitchgraphicsView3.scene().itemAt(QPointF(scene_pos), QTransform())
                    if type(item) is QGraphicsPixmapItem:
                        mouseX,mouseY = int(scene_pos.x()), int(scene_pos.y())
                        print(mouseX, mouseY)
                        self.pointSrc3.append((mouseX,mouseY))
                        self.displayImage(self.horizontalSlider3.value(), self.vidcap3, self.stitchgraphicsView3, self.pointSrc3)
                        # print(self.pointSrc3)
                        print("added ")
        return super().eventFilter(o, e)
    def displayImage2(self, frameNumber, vidcap, stitchgraphicsView, points):
        # self.removeGraphicsView.scene().clear()
        # if len(points)>0:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        success,image = vidcap.read()

        # displayImg = self.displayPoint(displayImg, self.pointSrc,(255,255,0))

        dim = (520, 350)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        for i in range(len(self.pointSrc2)):
            cv2.circle(image,self.pointSrc2[i],0,(255,255,0),5)
            cv2.putText(
                          img = image,
                          text = str(i),
                          org = self.pointSrc2[i],
                          fontFace = cv2.FONT_HERSHEY_DUPLEX,
                          fontScale = 0.5,
                          color = (125, 246, 55),
                          thickness = 1
                        )
        for i in range(len(self.pointSrc4)):
            cv2.circle(image,self.pointSrc4[i],0,(255,255,0),5)
            cv2.putText(
                          img = image,
                          text = str(i),
                          org = self.pointSrc4[i],
                          fontFace = cv2.FONT_HERSHEY_DUPLEX,
                          fontScale = 0.5,
                          color = (125, 246, 55),
                          thickness = 1)

            print('drawed')
        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 
        stitchgraphicsView.scene().addPixmap(pix)

    def displayImage(self, frameNumber, vidcap, stitchgraphicsView, points):
        # self.removeGraphicsView.scene().clear()
        # if len(points)>0:

        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        success,image = vidcap.read()

        # displayImg = self.displayPoint(displayImg, self.pointSrc,(255,255,0))

        dim = (520, 350)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        for i in range(len(points)):
            cv2.circle(image,points[i],0,(255,255,0),5)
            cv2.putText(
                          img = image,
                          text = str(i),
                          org = points[i],
                          fontFace = cv2.FONT_HERSHEY_DUPLEX,
                          fontScale = 0.5,
                          color = (125, 246, 55),
                          thickness = 1
                        )
            print('drawed')
        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 
        stitchgraphicsView.scene().addPixmap(pix)


    def loadFrame(self, frameNumber, vidcap, stitchgraphicsView):

        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        success,image = vidcap.read()

        scale_percent = 60 # percent of original size

        dim = (520, 350)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        b,g,r = cv2.split(image)           # get b, g, r
        rgb_img1 = cv2.merge([r,g,b])

        height, width, channel = rgb_img1.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img1.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap(qImg) 

        stitchgraphicsView.scene().addPixmap(pix)

    def preFrame(self, vidcap, horizontalSlider1, stitchgraphicsView, stitlLabel1, pointSrc):
        if pointSrc == self.pointSrc2:
            self.pointSrc4.clear()
            print('4 clear')

        pointSrc.clear()
        value = horizontalSlider1.value()
        if value > 0:
            value-=1
            horizontalSlider1.setValue(value)
            stitlLabel1.setText(str(value))
            self.loadFrame(horizontalSlider1.value(), vidcap, stitchgraphicsView)

    def nextFrame(self, vidcap, horizontalSlider1, stitchgraphicsView, stitlLabel1, pointSrc):
        if pointSrc == self.pointSrc2:
            self.pointSrc4.clear()
            print('4 clear')
        pointSrc.clear()
        value = horizontalSlider1.value()
        # if value < self.frameTotal:
        value+=1
        horizontalSlider1.setValue(value)
        stitlLabel1.setText(str(value))
        self.loadFrame(horizontalSlider1.value(), vidcap, stitchgraphicsView)
    
    def changed_slider1(self, vidcap, horizontalSlider1, stitchgraphicsView, stitlLabel1, pointSrc):
        pointSrc.clear()
        value = horizontalSlider1.value()
        stitlLabel1.setText(str(value))
        self.loadFrame(horizontalSlider1.value(), vidcap, stitchgraphicsView)

    def leftFun(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                     'All Files (*.*)')
        if path != ('', ''):
            print(path[0])

            self.leftEdit.setText(path[0])
            # img = cv2.imread(path[0])
            # self.images.append(img)
            self.path.append(path[0])

    def midFun(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                     'All Files (*.*)')
        if path != ('', ''):
            print(path[0])

            self.midEdit.setText(path[0])
            # img = cv2.imread(path[0])
            self.path.append(path[0])

    def rightFun(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                     'All Files (*.*)')
        if path != ('', ''):
            print(path[0])

            self.rightEdit.setText(path[0])
            # img = cv2.imread(path[0])
            self.path.append(path[0])


            
