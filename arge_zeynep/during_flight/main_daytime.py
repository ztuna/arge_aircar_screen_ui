import sys
import os
import csv
import functools
import math
import random
import time

from PyQt5 import QtCore, QtGui, QtWidgets, QtQml, QtQuick, QtQuickWidgets, QtWebChannel, QtWebEngineWidgets

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *

from widget.compass import CompassWidget
from widget.battery import BatteryWidget
from widget.speed import SpeedWidget
from widget.attitude import AttitudeWidget
from widget.altimeter import AltimeterWidget
from widget.variometer import VariometerWidget
from widget.turn   import TurnWidget
from widget.flight_duration import fDurationWidget

class GUI_MainWindow(QtWidgets.QMainWindow):
    os.chdir(os.path.dirname(os.path.realpath("during_flight")))       
    def __init__(self, parent=None):
        super().__init__() 
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.resize(screenSize.width(), screenSize.height())
        self.setStyleSheet("background-color: white")
        
        self.iteration=0
        self.batterySize=100        
        self.speedSize=0
        self.latVal = 0
        self.lngVal = 0
        self.f=open('vehicle_gps_position.csv','r')

        self.lat   = []
        self.lon   = []
        self.alt   = []
        self.dataReader()        
        
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("Central Widget")
        self.setCentralWidget(self.centralWidget)        
        
        dir_ = QtCore.QDir("Roboto_Slab")
        _id = QtGui.QFontDatabase.addApplicationFont("Roboto_Slab/RobotoSlab-SemiBold.ttf")
        
        palette = QtGui.QPalette()
        palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 0))
        palette.setColor(palette.Background, QtGui.QColor(255, 255, 255))
        
        # 0,0 = flight duration        
        durationTitle = QLabel()
        durationTitle.setObjectName("Duration Title")
        durationTitle.setText("Flight Duration")
        font  = durationTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        durationTitle.setFont(font)
        durationTitle.setPalette(palette)
        durationTitle.setAlignment(Qt.AlignCenter)

        self.durationIcon = fDurationWidget.fDuration(self)
        self.durationIcon.setObjectName("Duration Icon")
        self.durationIcon.reinit() 
        
        self.durationValue = QLabel()
        self.durationValue.setObjectName("Attitude Value")
        self.durationValue.setText("0:0:1")
        font  = self.durationValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.durationValue.setFont(font)
        self.durationValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.durationValue.setAlignment(Qt.AlignCenter)        
        
        groupBox1 = QGroupBox()        
        vbox1 = QVBoxLayout()  
        vbox1.addWidget(durationTitle)
        vbox1.addWidget(self.durationIcon)
        vbox1.addWidget(self.durationValue)
        vbox1.addStretch(1)
        groupBox1.setLayout(vbox1)
        groupBox1.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        # 0,1 = Air Speed Indicator
        speedTitle = QLabel()
        speedTitle.setObjectName("Speed Title")
        speedTitle.setText("Air Speed Indicator")
        font  = speedTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        speedTitle.setFont(font)
        speedTitle.setPalette(palette)   
        speedTitle.setAlignment(Qt.AlignCenter)        

        self.speedIcon = SpeedWidget.qfi_SI(self)
        self.speedIcon.setObjectName("Speed Icon")
        self.speedIcon.reinit()
        
        self.speedValue = QLabel()
        self.speedValue.setObjectName("Speed Value")
        self.speedValue.setText(str(2.0))
        font  = self.speedValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.speedValue.setFont(font)
        self.speedValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.speedValue.setAlignment(Qt.AlignCenter)        
        
        groupBox2 = QGroupBox()        
        vbox2 = QVBoxLayout()
        vbox2.addWidget(speedTitle)
        vbox2.addWidget(self.speedIcon)
        vbox2.addWidget(self.speedValue)
        vbox2.addStretch(1)
        groupBox2.setLayout(vbox2)
        groupBox2.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        # 0,2 = Attitude Indicator
        attitudeTitle = QLabel()
        attitudeTitle.setObjectName("Attitude Title")
        attitudeTitle.setText("Attitude Indicator")
        font  = attitudeTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        attitudeTitle.setFont(font)
        attitudeTitle.setPalette(palette) 
        attitudeTitle.setAlignment(Qt.AlignCenter)        

        self.attitudeIcon = AttitudeWidget.Attitude(self)
        self.attitudeIcon.setObjectName("Attitude Icon")
        self.attitudeIcon.reinit()
        
        self.attitudeValue = QLabel()
        self.attitudeValue.setObjectName("Attitude Value")
        self.attitudeValue.setText(str(1.0))
        font  = self.attitudeValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.attitudeValue.setFont(font)
        self.attitudeValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.attitudeValue.setAlignment(Qt.AlignCenter)                
        
        groupBox3 = QGroupBox()        
        vbox3 = QVBoxLayout()
        vbox3.addWidget(attitudeTitle)
        vbox3.addWidget(self.attitudeIcon)
        vbox3.addWidget(self.attitudeValue)
        vbox3.addStretch(1)
        groupBox3.setLayout(vbox3)
        groupBox3.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        # 0,3 = Altimeter
        altimeterTitle = QLabel()
        altimeterTitle.setObjectName("Altimeter Title")
        altimeterTitle.setText("Altimeter")
        font  = altimeterTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        altimeterTitle.setFont(font)
        altimeterTitle.setPalette(palette)  
        altimeterTitle.setAlignment(Qt.AlignCenter)        

        self.altimeterIcon = AltimeterWidget.Altimeter(self)
        self.altimeterIcon.setObjectName("Altimeter Icon")
        self.altimeterIcon.reinit()
        
        self.altimeterValue = QLabel()
        self.altimeterValue.setObjectName("Attitude Value")
        self.altimeterValue.setText(str(1.0))
        font  = self.altimeterValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.altimeterValue.setFont(font)
        self.altimeterValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.altimeterValue.setAlignment(Qt.AlignCenter)  
    
        groupBox4 = QGroupBox()        
        vbox4 = QVBoxLayout()
        vbox4.addWidget(altimeterTitle)
        vbox4.addWidget(self.altimeterIcon)
        vbox4.addWidget(self.altimeterValue)
        vbox4.addStretch(1)
        groupBox4.setLayout(vbox4)
        groupBox4.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        

        # 1,0 = Remaining Battery
        batteryTitle = QLabel()
        batteryTitle.setObjectName("Battery Title")
        batteryTitle.setText("Remaining Battery")
        font  = batteryTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        batteryTitle.setFont(font)
        batteryTitle.setPalette(palette) 
        batteryTitle.setAlignment(Qt.AlignCenter)        
        
        self.batteryIcon = BatteryWidget.Battery(self)
        self.batteryIcon.setObjectName("Battery Icon")
        self.batteryIcon.reinit()        
        
        self.batteryValue = QLabel()
        self.batteryValue.setObjectName("Attitude Value")
        self.batteryValue.setText(str(self.batterySize))
        font  = self.batteryValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.batteryValue.setFont(font)
        self.batteryValue.setAlignment(Qt.AlignCenter)
        self.batteryValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
    
        groupBox5 = QGroupBox()   
        vbox5 = QVBoxLayout()
        vbox5.addWidget(batteryTitle)
        vbox5.addWidget(self.batteryIcon)
        vbox5.addWidget(self.batteryValue)
        vbox5.addStretch(1)
        groupBox5.setLayout(vbox5)
        groupBox5.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")           
                
        # 1,1 = Turn and Slip Indicator
        turnSlipTitle = QLabel()
        turnSlipTitle.setObjectName("TurnSlip Title")
        turnSlipTitle.setText("Turn and Slip Indicator")
        font  = turnSlipTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        turnSlipTitle.setFont(font)
        turnSlipTitle.setPalette(palette) 
        turnSlipTitle.setAlignment(Qt.AlignCenter)        

        self.turnSlipIcon = TurnWidget.Turn(self)
        self.turnSlipIcon.setObjectName("TurnSlip Icon")
        self.turnSlipIcon.reinit()
        
        self.turnSlipValue = QLabel()
        self.turnSlipValue.setObjectName("Attitude Value")
        self.turnSlipValue.setText(str(1.0))
        font  = self.turnSlipValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.turnSlipValue.setFont(font)
        self.turnSlipValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.turnSlipValue.setAlignment(Qt.AlignCenter)  
        
        groupBox6 = QGroupBox()        
        vbox6 = QVBoxLayout()
        vbox6.addWidget(turnSlipTitle)
        vbox6.addWidget(self.turnSlipIcon)
        vbox6.addWidget(self.turnSlipValue)
        vbox6.addStretch(1)
        groupBox6.setLayout(vbox6)
        groupBox6.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        # 1,2 = Heading Indicator
        headingTitle = QLabel()
        headingTitle.setObjectName("Heading Title")
        headingTitle.setText("Heading Indicator")
        font  = headingTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        headingTitle.setFont(font)
        headingTitle.setPalette(palette) 
        headingTitle.setAlignment(Qt.AlignCenter)        

        self.headingIcon = CompassWidget.qfi_HSI(self)
        self.headingIcon.setObjectName("Heading Icon")
        self.headingIcon.reinit()
        
        self.headingValue = QLabel()
        self.headingValue.setObjectName("Attitude Value")
        self.headingValue.setText(str(1.0))
        font  = self.headingValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.headingValue.setFont(font)
        self.headingValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.headingValue.setAlignment(Qt.AlignCenter)  
        
        groupBox7 = QGroupBox()        
        vbox7 = QVBoxLayout()
        vbox7.addWidget(headingTitle)
        vbox7.addWidget(self.headingIcon)
        vbox7.addWidget(self.headingValue)
        vbox7.addStretch(1)
        groupBox7.setLayout(vbox7)
        groupBox7.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        # 1,3 = Variometer
        variometerTitle = QLabel()
        variometerTitle.setObjectName("Variometer Title")
        variometerTitle.setText("Variometer")
        font  = variometerTitle.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)    
        variometerTitle.setFont(font)
        variometerTitle.setPalette(palette)
        variometerTitle.setAlignment(Qt.AlignCenter)        

        self.variometerIcon = VariometerWidget.Variometer(self)
        self.variometerIcon.setObjectName("Heading Icon")
        self.variometerIcon.reinit()
        
        self.variometerValue = QLabel()
        self.variometerValue.setObjectName("Attitude Value")
        self.variometerValue.setText(str(1.0))
        font  = self.variometerValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.variometerValue.setFont(font)
        self.variometerValue.setStyleSheet("QLabel { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(0, 0, 0); color: rgb(0, 0, 255); }")
        self.variometerValue.setAlignment(Qt.AlignCenter)  

        groupBox8 = QGroupBox()                
        vbox8 = QVBoxLayout()
        vbox8.addWidget(variometerTitle)
        vbox8.addWidget(self.variometerIcon)
        vbox8.addWidget(self.variometerValue)
        vbox8.addStretch(1)
        groupBox8.setLayout(vbox8)
        groupBox8.setStyleSheet("QGroupBox { background-color: \
        rgb(255, 255, 255); border: 3px solid rgb(255, 255, 255); }")        
        
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 0, 1)
        grid.addWidget(groupBox3, 0, 2)
        grid.addWidget(groupBox4, 0, 3)
        grid.addWidget(groupBox5, 1, 0)
        grid.addWidget(groupBox6, 1, 1)
        grid.addWidget(groupBox7, 1, 2)
        grid.addWidget(groupBox8, 1, 3)
        
        self.centralWidget.setLayout(grid)
        
        self.timeWidget = QtWidgets.QLabel(self.centralWidget)
        hPosition1 = self.takePercentage(93.75, screenSize.width())
        vPosition1 = self.takePercentage(0.5, screenSize.height())
        self.timeWidget.setGeometry(QtCore.QRect(hPosition1, vPosition1, 80, 50))
    
        self.timeWidget.setText(self.getTime())
        font = self.timeWidget.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(30) 
        self.timeWidget.setFont(font)
        self.timeWidget.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        self.showFullScreen()        
 
    def speedCalculate(self):
        speed = math.sqrt( (self.lon[self.iteration]-self.lon[self.iteration-1])**2 + (self.lat[self.iteration]-self.lat[self.iteration-1])**2  )
        return speed

    def setViewWidget(self):
        self.iteration += 1
        self.speedSize += 1
        self.batterySize -= 1
        if self.batterySize < 0:
            self.batterySize = 100
        if self.speedSize > 16:
            self.speedSize = 0   
    
        self.headingIcon.setHeading(30)
        self.speedIcon.setSpeed(12)        
        self.altimeterIcon.setAltitude(self.alt[self.iteration])
        self.attitudeIcon.setRoll(10*math.cos(45))
        self.attitudeIcon.setPitch(10*math.cos(45))
        self.variometerIcon.setClimbRate(100)
        self.turnSlipIcon.setTurnRate(10*math.cos(45))
        self.turnSlipIcon.setSlipSkid(10*math.cos(45))
        self.durationIcon.setHour(self.timerEvent().hour())
        self.durationIcon.setMin(self.timerEvent().minute())
        self.durationIcon.setSec(self.timerEvent().second())
        self.batteryIcon.setCurrentVal(self.batterySize)
    
    
        self.headingIcon.viewUpdate.emit()
        self.speedIcon.viewUpdate.emit()
        self.altimeterIcon.viewUpdate.emit()
        self.attitudeIcon.viewUpdate.emit()
        self.variometerIcon.viewUpdate.emit()
        self.turnSlipIcon.viewUpdate.emit()
        self.durationIcon.viewUpdate.emit()
        self.batteryIcon.viewUpdate.emit()
    
    
        self.attitudeValue.setText(str(45))
        self.speedValue.setText(str(12))
        self.batteryValue.setText(str(self.batterySize) + "%")
        self.altimeterValue.setText(str(self.alt[self.iteration]))
        self.variometerValue.setText(str(100))
        self.turnSlipValue.setText(str(10*math.cos(45)))
        self.headingValue.setText(str(30))
        self.durationValue.setText(self.timerEvent().toString("hh:mm:ss"))

        self.LogPrint()
        
    def timerEvent(self):
        global time
        time = time.addSecs(1)
        return time
        
    def getTime(self):
        now = time.localtime()
        hour = str(now[3])
        min = str(now[4])
        if len(hour) == 1:
            hour = "0" + hour
        if len(min) == 1:
            min = "0" + min
        digitalTime = hour + ":" + min
        return digitalTime
    
    def takePercentage(self, percent, whole):
        return (percent * whole) / 100.0    
    def dataReader(self):
        with self.f:
            reader = csv.DictReader(self.f)
    
            for row in reader:
                self.lat.append(float(row['lat']))
                self.lon.append(float(row['lon']))
                self.alt.append(float(row['alt']))
                
    def LogPrint(self):
            print("*****Location Lon*****")
            print(self.lon[self.iteration])
            print("*****Location Lat*****")
            print(self.lat[self.iteration])
            print("*****Altimeter M*****")
            print(self.alt[self.iteration])

window = GUI_MainWindow()    #Main window written in pyqt5

timer = QtCore.QTimer()
time = QtCore.QTime(0, 0, 0)
timer.timeout.connect(window.timerEvent)
timer.start(200)

timer2 = QtCore.QTimer()
timer2.timeout.connect(window.setViewWidget)
timer2.start(200)
window.show()