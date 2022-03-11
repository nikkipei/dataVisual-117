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


class VisualOverview(QWidget):
    def __init__(self, speed1Layout, speed2Layout, volumeLayout, headway1OverLayout, headway2OverLayout, parent=None):
        super().__init__(parent)
        ##############overview tab#################
        # visualGraphicsView.scene().addPixmap(pix)
        width = 380
        height = 350
        self.speed1Layout = speed1Layout
        self.speed2Layout = speed2Layout
        self.volumeLayout = volumeLayout
        self.headway1OverLayout = headway1OverLayout
        self.headway2OverLayout = headway2OverLayout

        #self.speed1Layout
        self.graphOverSpeed = pg.PlotWidget()
        self.graphOverSpeed.setFixedWidth(width)
        self.graphOverSpeed.setFixedHeight(height)

        self.graphOverSpeed.setLabel('left', 'Temperature (°C)')
        self.graphOverSpeed.setLabel('bottom', 'Hour (H)')
        self.graphOverSpeed.showGrid(x=True, y=True)
        self.speed1Layout.addWidget(self.graphOverSpeed)

        pen = pg.mkPen(color= 'g', width=3)
        hour = [5,10,15,20,15,30,35,40]
        temperature = [30,32,34,32,33,31,29,32]
        self.graphOverSpeed.plot(hour, temperature, name="Sensor 1",  pen=pen, 
                                        symbol='o', symbolSize=8, symbolBrush=('g'))
        self.graphOverSpeed.plot(hour, temperature, pen=pen)


        #speed2Layout
        self.graphOverSpeed2 = pg.PlotWidget()
        self.graphOverSpeed2.setFixedWidth(width)
        self.graphOverSpeed2.setFixedHeight(height)

        self.graphOverSpeed2.setLabel('left', 'Temperature (°C)')
        self.graphOverSpeed2.setLabel('bottom', 'Hour (H)')
        self.graphOverSpeed2.showGrid(x=True, y=True)
        self.speed2Layout.addWidget(self.graphOverSpeed2)
        pen = pg.mkPen(color= 'c', width=3)
        hour = [5,10,15,20,15,30,35,40]
        temperature = [30,32,34,32,33,31,29,32]
        self.graphOverSpeed2.plot(hour, temperature, name="Sensor 1",  pen=pen, 
                                        symbol='o', symbolSize=8, symbolBrush=('c'))
        self.graphOverSpeed2.plot(hour, temperature, pen=pen)


        self.graphOvervolume = pg.PlotWidget()
        self.graphOvervolume.setFixedWidth(width)
        self.graphOvervolume.setFixedHeight(height)

        self.graphOvervolume.setLabel('left', 'Temperature (°C)')
        self.graphOvervolume.setLabel('bottom', 'Hour (H)')
        self.graphOvervolume.showGrid(x=True, y=True)
        self.volumeLayout.addWidget(self.graphOvervolume)
        pen = pg.mkPen(color= 'r', width=3)
        hour = [5,10,15,20,15,30,35,40]
        temperature = [30,32,34,32,33,31,29,32]
        self.graphOvervolume.plot(hour, temperature, name="Sensor 1",  pen=pen, 
                                        symbol='o', symbolSize=8, symbolBrush=('r'))
        self.graphOvervolume.plot(hour, temperature, pen=pen)


