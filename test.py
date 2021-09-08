#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtCore import QUrl
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)

        self.webEngineView = QWebEngineView()
        self.loadPage()

        vbox.addWidget(self.webEngineView)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 1250, 900)
        self.setWindowTitle('QWebEngineView')
        self.show()

    def loadPage(self):
        self.webEngineView.load(QUrl.fromUserInput("http://127.0.0.1:8085/test.html"))

        # with open('www.baidu.com', 'r') as f:

        #     html = f.read()
        #     self.webEngineView.setHtml(html)
        #     self.webEngineView.

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()