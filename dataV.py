from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://api.mapbox.com/styles/v1/nikkipei/cksqn08nj1dk417mrb3ryqx5p.html?fresh=true&title=view&access_token=pk.eyJ1Ijoibmlra2lwZWkiLCJhIjoiY2tzcDJqMm85MDFvNDJ3cDc0MXhkeWFhaCJ9.vK5iDtMm7eZ5q6Gwtt1UDw"))

        self.setCentralWidget(self.browser)

        self.show()

app = QApplication(sys.argv)
window = MainWindow()

app.exec_()