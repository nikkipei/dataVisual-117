from editor import (
    Editor,
    TOOL_ADD_ARC,
    TOOL_ADD_REGION,
    TOOL_REMOVE_ARC,
    TOOL_REMOVE_REGION,
    loadCSV,
    saveCSV,
)
# from visualizator import *
from stitcher import *
from convertor import *
from remover import *
from stable import *
from VisualIndividual import*
from VisualOverview import*
from selectLane import*
import os
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from player import Player
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

video_parentGPS = window.findChild(QWidget, "videoParentGPS")
videoStable = window.findChild(QWidget, "videoStab")
removeVideoParentswidget = window.findChild(QWidget, "removeVideoParentswidget")
videoParentSelect= window.findChild(QWidget, "videoParentSelect")

stitchvideoParents = window.findChild(QWidget, "stichvideoParents")

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
# video_parentGPS.layout().addWidget(player, 0, 0)

video_next_btn.clicked.connect(lambda: player.nextFrame())
video_pause_btn.clicked.connect(lambda: player.pause())
video_play_btn.clicked.connect(lambda: player.play())
video_previous_btn.clicked.connect(lambda: player.prevFrame())
video_stop_btn.clicked.connect(lambda: player.stop())


scroll = window.findChild(QScrollArea, "scrollAreaLine")
widget = QWidget() 


# vbox = QVBoxLayout()
vbox = QGridLayout()
widget.setLayout(vbox)
scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
scroll.setWidgetResizable(True)
scroll.setWidget(widget)

xy_save_btn = window.findChild(QPushButton, "xySavebtn")
editConv = window.findChild(QPushButton, "editConvert")
deleteConv = window.findChild(QPushButton, "deleteConve")
onlyInt = QDoubleValidator()
convPointsLabel = window.findChild(QPlainTextEdit, "convPointsLabel")
convertResLabel = window.findChild(QPlainTextEdit, "convertResLabel")
verifyMapbtn = window.findChild(QPushButton, "verifyMapbtn")

# stable
stabLoadVideobtn = window.findChild(QPushButton, "loadStabVideobtn")
restartBtn = window.findChild(QPushButton, "restartBtn")

graphicsViewStab = window.findChild(QGraphicsView, "graphicsView")

#Remove()
removeGraphicsView = window.findChild(QGraphicsView, "removeGraphicsView")
addBtn = window.findChild(QPushButton, "addBtn")
redoBtn = window.findChild(QPushButton, "redoBtn")
deleteBtn = window.findChild(QPushButton, "deleteBtn")
finishBtn = window.findChild(QPushButton, "finishBtn")
restartRMBtn = window.findChild(QPushButton, "restartRMBtn")

#stich

stitchgraphicsView = window.findChild(QGraphicsView, "stitchgraphicsView1")
stitchgraphicsView2 = window.findChild(QGraphicsView, "stitchgraphicsView2")
stitchgraphicsView3 = window.findChild(QGraphicsView, "stitchgraphicsView3")
graphicsView_2 = window.findChild(QGraphicsView, "graphicsView_2")

leftBtn = window.findChild(QPushButton, "leftBtn")
midBtn = window.findChild(QPushButton, "midBtn")
rightBtn = window.findChild(QPushButton, "rightBtn")
loadBtn = window.findChild(QPushButton, "loadBtn")
leftEdit = window.findChild(QTextEdit, "leftEdit")
midEdit = window.findChild(QTextEdit, "midEdit")
rightEdit = window.findChild(QTextEdit, "rightEdit")

horizontalSlider1 = window.findChild(QSlider, "horizontalSlider1")
stitlLabel1 = window.findChild(QLabel, "stitlLabel1")
prevBtn1 = window.findChild(QPushButton, "prevBtn1")
nextBtn1 = window.findChild(QPushButton, "nextBtn1")

horizontalSlider2 = window.findChild(QSlider, "horizontalSlider2")
stitlLabel2 = window.findChild(QLabel, "stitlLabel2")
prevBtn2 = window.findChild(QPushButton, "prevBtn2")
nextBtn2 = window.findChild(QPushButton, "nextBtn2")

horizontalSlider3 = window.findChild(QSlider, "horizontalSlider3")
stitlLabel3 = window.findChild(QLabel, "stitlLabel3")
prevBtn3 = window.findChild(QPushButton, "prevBtn3")
nextBtn3 = window.findChild(QPushButton, "nextBtn3")

matchColorChecked1 = window.findChild(QCheckBox, "checkBox_1")
matchColorChecked2 = window.findChild(QCheckBox, "checkBox_2")
matchColorChecked3 = window.findChild(QCheckBox, "checkBox_3")
redo1btn = window.findChild(QPushButton, "redo1btn")
redo2btn = window.findChild(QPushButton, "redo2btn")
redo4btn = window.findChild(QPushButton, "redo4btn")
redo3btn = window.findChild(QPushButton, "redo3btn")
previewBtn = window.findChild(QPushButton, "previewBtn")
startBtn = window.findChild(QPushButton, "startBtn")
backBtn = window.findChild(QPushButton, "backBtn")


editor = Editor(player, car_id_edit, car_info_save_btn, video_parent)
video_parent.layout().addWidget(editor, 0, 0)
editor.raise_()

stitcher = Stitcher(stitchgraphicsView, prevBtn1, nextBtn1,stitchgraphicsView2, 
    prevBtn2, nextBtn2, stitchgraphicsView3, prevBtn3, nextBtn3, 
    leftBtn, midBtn, rightBtn, loadBtn, leftEdit, midEdit, rightEdit, 
    horizontalSlider2, stitlLabel1, horizontalSlider1, stitlLabel2, 
    horizontalSlider3, stitlLabel3, graphicsView_2, matchColorChecked1,
    matchColorChecked2, matchColorChecked3, redo1btn, redo2btn, redo4btn, redo3btn, 
    previewBtn, startBtn, backBtn)

stitchvideoParents.layout().addWidget(stitcher, 0, 0)

#select lanes
lineSelectGV = window.findChild(QGraphicsView, "lineSelectGV")
laneAddBtn = window.findChild(QPushButton, "laneAddBtn")
laneRedoBtn = window.findChild(QPushButton, "laneRedoBtn")
laneDeleteBtn = window.findChild(QPushButton, "laneDeleteBtn")
laneFinishBtn = window.findChild(QPushButton, "laneFinishBtn")
lanerestartBtn= window.findChild(QPushButton, "LanerestartBtn")

selectLane = SelectLane(lineSelectGV, laneAddBtn, laneRedoBtn,laneDeleteBtn, laneFinishBtn, lanerestartBtn)
videoParentSelect.layout().addWidget(selectLane, 0, 0)
selectLane.raise_()



# visual tab
stackedWidget = window.findChild(QStackedWidget, "stackedWidget")
visualPreFramebtn = window.findChild(QPushButton, "visualPreFramebtn")
visualNextFramebtn = window.findChild(QPushButton, "visualNextFramebtn")
visualGraphicsView = window.findChild(QGraphicsView, "visualGraphicsView")
visualSlider = window.findChild(QSlider, "visualSlider")
visualLabel = window.findChild(QLabel, "visualLabel")
carIDdisplay = window.findChild(QLineEdit, "carIDdisplay")
carTypeDisplay = window.findChild(QLineEdit, "carTypeDisplay")
visualverticalLayout = window.findChild(QGridLayout, "visualverticalLayout")
visualTrajectverticalLayout  = window.findChild(QGridLayout, "visualTrajectverticalLayout")
visualHeadwayverticalLayout  = window.findChild(QGridLayout, "visualHeadwayverticalLayout")
playBtn = window.findChild(QPushButton, "playBtn")
pauseBtn = window.findChild(QPushButton, "pauseBtn")
stopBtn = window.findChild(QPushButton, "stopBtn")

#overview tab
#speed1Layout, speed2Layout, volumeLayout, headway1OverLayout, headway2OverLayout
speed1Layout = window.findChild(QGridLayout, "speed1Layout")
speed2Layout = window.findChild(QGridLayout, "speed2Layout") 
volumeLayout = window.findChild(QGridLayout, "volumeLayout") 
headway1OverLayout = window.findChild(QGridLayout, "headway1OverLayout") 
headway2OverLayout = window.findChild(QGridLayout, "headway2OverLayout") 


#switch between tabs
overviewbtn1 = window.findChild(QPushButton, "overviewbtn1")
individualbtn1 = window.findChild(QPushButton, "individualbtn1")
analysisbtn1 = window.findChild(QPushButton, "analysisbtn1")

overviewbtn2 = window.findChild(QPushButton, "overviewbtn2")
individualbtn2 = window.findChild(QPushButton, "individualbtn2")
analysisbtn2 = window.findChild(QPushButton, "analysisbtn2")

overviewbtn3 = window.findChild(QPushButton, "overviewbtn3")
individualbtn3 = window.findChild(QPushButton, "individualbtn3")
analysisbtn3 = window.findChild(QPushButton, "analysisbtn3")
# stackedWidget.setCurrentIndex(1)
# overviewbtn.clicked.connect(lambda:stackedWidget.setCurrentIndex(1))
# overviewbtn.clicked.connect(overviww())
laneWebEngineView = window.findChild(QWebEngineView, "laneWebEngineView")

VisualIndividual = VisualIndividual(visualGraphicsView, visualverticalLayout, visualTrajectverticalLayout, visualHeadwayverticalLayout, 
                visualPreFramebtn,visualNextFramebtn, visualSlider,visualLabel, carIDdisplay, 
                carTypeDisplay,playBtn, pauseBtn, stopBtn, laneWebEngineView)
VisualIndividual.raise_()

VisualOverview = VisualOverview(speed1Layout, speed2Layout, volumeLayout, headway1OverLayout, headway2OverLayout)
VisualOverview.raise_()


csv_path = None

def overviewFun():
    # print('overviewFun')
    stackedWidget.setCurrentIndex(0)
overviewbtn1.clicked.connect(overviewFun)
overviewbtn2.clicked.connect(overviewFun)
overviewbtn3.clicked.connect(overviewFun)

def individualFun():
    # print('individualFun')
    stackedWidget.setCurrentIndex(1)
individualbtn1.clicked.connect(individualFun)
individualbtn2.clicked.connect(individualFun)
individualbtn3.clicked.connect(individualFun)

def analysisFun():
    # print('analysisFun')
    stackedWidget.setCurrentIndex(2)
analysisbtn1.clicked.connect(analysisFun)
analysisbtn2.clicked.connect(analysisFun)
analysisbtn3.clicked.connect(analysisFun)

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
        data = loadCSV(csv_path)
        editor.setData(data)
        # webEngineView.setHtml(htmldataVisual(csv_path) )
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
        convetor = Convertor(player, path, video_parentGPS, vbox, verifyMapbtn, convertResLabel, convPointsLabel, xy_save_btn, editConv, deleteConv, video_parent)
        video_parentGPS.layout().addWidget(convetor, 0, 0)
        convetor.raise_()

        stabletor = Stabilization(path, videoStable, stabLoadVideobtn, graphicsViewStab, restartBtn)
        videoStable.layout().addWidget(stabletor, 0, 0)

        remover = Remover(path, removeVideoParentswidget, removeGraphicsView, addBtn, redoBtn, deleteBtn, finishBtn, restartRMBtn)
        removeVideoParentswidget.layout().addWidget(remover, 0, 0)

def onSaveCSV():
    global csv_path
    if csv_path:
        print(f"Saving CSV: {csv_path}")
        data = editor.getData()
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


def onLoad():
    frames_slider.setRange(0, player.frame_count - 1)
    frames_count_label.setText(f"/ {player.frame_count-1}")
    frame_spin_box.setRange(0, player.frame_count - 1)

# web engine View
dataVS = window.findChild(QVBoxLayout, "webpage")
webEngineView = QWebEngineView()

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
