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
    def __init__(self, parent=None):
        super().__init__() 
        self.resize(1440, 900)
        self.setStyleSheet("background-color: black")
        
        self.iteration = 0
        self.batterySize = 100        
        self.speedSize = 0
        self.latVal = 0
        self.lngVal = 0
        self.file = open('mavlink_msg.txt','r')

        self.lat   = []
        self.lon   = []
        self.alt   = []
        self.speed = []
        self.vspeed = []
        self.roll = []
        self.pitch = []
        self.heading = []
        self.dataReader()        
        
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("Central Widget")
        self.setCentralWidget(self.centralWidget)        
        
        dir_ = QtCore.QDir("Roboto_Slab")
        _id = QtGui.QFontDatabase.addApplicationFont("Roboto_Slab/RobotoSlab-SemiBold.ttf")
        
        palette = QtGui.QPalette()
        palette.setColor(palette.Background, QtGui.QColor(0, 0, 0))
        palette.setColor(palette.WindowText, QtGui.QColor(255, 255, 255))
        
        # 0,0 = Flight Duration Indicator       
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
        self.durationIcon.resize(307, 327.5)        
        self.durationIcon.reinit() 
        
        self.durationValue = QLabel()
        self.durationValue.setObjectName("Duration Value")
        self.durationValue.setText("00:00:01")
        font  = self.durationValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.durationValue.setFont(font)
        self.durationValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.durationValue.setAlignment(Qt.AlignCenter)        
        
        duration = QGroupBox()        
        durationLayout = QVBoxLayout()  
        durationLayout.addWidget(durationTitle)
        durationLayout.addWidget(self.durationIcon)
        durationLayout.addWidget(self.durationValue)
        durationLayout.addStretch(1)
        duration.setLayout(durationLayout)
        duration.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")       
        duration.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                
        
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
        self.speedIcon.resize(307, 320)                
        self.speedIcon.reinit()
        
        self.speedValue = QLabel()
        self.speedValue.setObjectName("Speed Value")
        self.speedValue.setText(str(0.0))
        font  = self.speedValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.speedValue.setFont(font)
        self.speedValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.speedValue.setAlignment(Qt.AlignCenter)   
        
        speed = QGroupBox()        
        speedLayout = QVBoxLayout()
        speedLayout.addWidget(speedTitle)
        speedLayout.addWidget(self.speedIcon)
        speedLayout.addWidget(self.speedValue)
        speedLayout.addStretch(1)
        speed.setLayout(speedLayout)
        speed.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }") 
        speed.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                        
        
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
        self.attitudeIcon.resize(307, 320)                
        self.attitudeIcon.reinit()
        
        self.attitudeValue = QLabel()
        self.attitudeValue.setObjectName("Attitude Value")
        self.attitudeValue.setText(str(0.0))
        font  = self.attitudeValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.attitudeValue.setFont(font)
        self.attitudeValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.attitudeValue.setAlignment(Qt.AlignCenter)                
        
        attitude = QGroupBox()        
        attitudeLayout = QVBoxLayout()
        attitudeLayout.addWidget(attitudeTitle)
        attitudeLayout.addWidget(self.attitudeIcon)
        attitudeLayout.addWidget(self.attitudeValue)
        attitudeLayout.addStretch(1)
        attitude.setLayout(attitudeLayout)
        attitude.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")   
        attitude.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                
        
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
        self.altimeterIcon.resize(307, 318)                
        self.altimeterIcon.reinit()
        
        self.altimeterValue = QLabel()
        self.altimeterValue.setObjectName("Attitude Value")
        self.altimeterValue.setText(str(0.0))
        font  = self.altimeterValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.altimeterValue.setFont(font)
        self.altimeterValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.altimeterValue.setAlignment(Qt.AlignCenter)  
    
        altimeter = QGroupBox()        
        altimeterLayout = QVBoxLayout()
        altimeterLayout.addWidget(altimeterTitle)
        altimeterLayout.addWidget(self.altimeterIcon)
        altimeterLayout.addWidget(self.altimeterValue)
        altimeterLayout.addStretch(1)
        altimeter.setLayout(altimeterLayout)
        altimeter.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")      
        altimeter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                

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
        self.batteryIcon.resize(307, 323)                
        self.batteryIcon.reinit()
        
        self.batteryValue = QLabel()
        self.batteryValue.setObjectName("Battery Value")
        self.batteryValue.setText(str(self.batterySize))
        font  = self.batteryValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.batteryValue.setFont(font)
        self.batteryValue.setAlignment(Qt.AlignCenter)
        self.batteryValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
    
        battery = QGroupBox()   
        batteryLayout = QVBoxLayout()
        batteryLayout.addWidget(batteryTitle)
        batteryLayout.addWidget(self.batteryIcon)
        batteryLayout.addWidget(self.batteryValue)
        batteryLayout.addStretch(1)
        battery.setLayout(batteryLayout)
        battery.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")        
        battery.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                
        
        # 1,1 = Heading Indicator
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
        self.headingIcon.resize(307, 316)            
        self.headingIcon.reinit()
        
        self.headingValue = QLabel()
        self.headingValue.setObjectName("Attitude Value")
        self.headingValue.setText(str(0.0))
        font  = self.headingValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.headingValue.setFont(font)
        self.headingValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.headingValue.setAlignment(Qt.AlignCenter)  
        
        heading = QGroupBox()        
        headingLayout = QVBoxLayout()
        headingLayout.addWidget(headingTitle)
        headingLayout.addWidget(self.headingIcon)
        headingLayout.addWidget(self.headingValue)
        headingLayout.addStretch(1)
        heading.setLayout(headingLayout)
        heading.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")    
        heading.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                
        
        # 1,2 = Variometer
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
        self.variometerIcon.resize(307, 316)                
        self.variometerIcon.reinit()
        
        self.variometerValue = QLabel()
        self.variometerValue.setObjectName("Attitude Value")
        self.variometerValue.setText(str(1.0))
        font  = self.variometerValue.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(25)    
        self.variometerValue.setFont(font)
        self.variometerValue.setStyleSheet("QLabel { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(255, 255, 255); color: rgb(0, 255, 0); }")
        self.variometerValue.setAlignment(Qt.AlignCenter)  

        variometer = QGroupBox()                
        variometerLayout = QVBoxLayout()
        variometerLayout.addWidget(variometerTitle)
        variometerLayout.addWidget(self.variometerIcon)
        variometerLayout.addWidget(self.variometerValue)
        variometerLayout.addStretch(1)
        variometer.setLayout(variometerLayout)
        variometer.setStyleSheet("QGroupBox { background-color: \
        rgb(0, 0, 0); border: 3px solid rgb(0, 0, 0); }")        
        variometer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)                        
        
        centralBox = QVBoxLayout()
        topBox = QHBoxLayout()
        bottomBox = QHBoxLayout()
        centralBox.addLayout(topBox)
        centralBox.addLayout(bottomBox)
        
        durationBox = QVBoxLayout()
        durationBox.addWidget(duration)
        speedBox = QVBoxLayout()
        speedBox.addWidget(speed)
        attitudeBox = QVBoxLayout()
        attitudeBox.addWidget(attitude)
        altimeterBox = QVBoxLayout()
        altimeterBox.addWidget(altimeter)
        batteryBox = QVBoxLayout()
        batteryBox.addWidget(battery)
        headingBox = QVBoxLayout()
        headingBox.addWidget(heading)
        variometerBox = QVBoxLayout()
        variometerBox.addWidget(variometer)        
        
        topBox.addLayout(durationBox)
        topBox.addLayout(speedBox)        
        topBox.addLayout(attitudeBox)
        topBox.addLayout(altimeterBox)
        bottomBox.addLayout(batteryBox)
        bottomBox.addLayout(headingBox)
        bottomBox.addLayout(variometerBox)
        bottomBox.setAlignment(Qt.AlignCenter)
        bottomBox.setContentsMargins(195, 0, 195, 0)
        
        self.centralWidget.setLayout(centralBox)
        
        self.timeWidget = QtWidgets.QLabel(self.centralWidget)
        self.timeWidget.setGeometry(QtCore.QRect(1350, 4.5, 80, 50))
    
        self.timeWidget.setText(self.getTime())
        font = self.timeWidget.font()
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(30) 
        self.timeWidget.setFont(font)
        self.timeWidget.setPalette(palette)
        self.timeWidget.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        self.showFullScreen()        

    def setViewWidget(self):
        self.iteration += 1
        self.batterySize -= 1
        if self.batterySize < 0:
            self.batterySize = 100

        try:
            self.headingIcon.setHeading(self.heading[self.iteration])
            self.speedIcon.setSpeed(self.speed[self.iteration])        
            self.altimeterIcon.setAltitude(self.alt[self.iteration])
            self.attitudeIcon.setRoll(self.roll[self.iteration])
            self.attitudeIcon.setPitch(self.pitch[self.iteration])
            self.variometerIcon.setClimbRate(self.vspeed[self.iteration])
            self.durationIcon.setHour(self.timerEvent().hour())
            self.durationIcon.setMin(self.timerEvent().minute())
            self.durationIcon.setSec(self.timerEvent().second())
            self.batteryIcon.setCurrentVal(self.batterySize)
        except IndexError:
            sys.exit()
                
        self.headingIcon.viewUpdate.emit()
        self.speedIcon.viewUpdate.emit()
        self.altimeterIcon.viewUpdate.emit()
        self.attitudeIcon.viewUpdate.emit()
        self.variometerIcon.viewUpdate.emit()
        self.durationIcon.viewUpdate.emit()
        self.batteryIcon.viewUpdate.emit()
        
        self.attitudeValue.setText("Roll = " + str("{:.2f}".format(self.roll[self.iteration])) + ", Pitch = " + str("{:.2f}".format(self.roll[self.iteration])))
        self.speedValue.setText(str("{:.2f}".format(self.speed[self.iteration])))
        self.batteryValue.setText(str(self.batterySize) + "%")
        self.altimeterValue.setText(str("{:.2f}".format(self.alt[self.iteration])))
        self.variometerValue.setText(str("{:.2f}".format(self.vspeed[self.iteration])))
        self.headingValue.setText(str("{:.2f}".format(self.heading[self.iteration])))
        self.durationValue.setText(self.timerEvent().toString("hh:mm:ss"))

        self.LogPrint()
        
    def timerEvent(self):
        global time
        time = time.addMSecs(200)
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
    
    def dataReader(self):
        with self.file:
            date = self.file.readline().split(',')[-2][10:-6]
            for line in self.file:
                nextDate = line.split(',')[-2][10:-6]
                if nextDate == date:
                    curAlt = 0
                    curSpeed = 0
                    curVSpeed = 0
                    curHeading = 0
                    curRoll = 0
                    curPitch = 0            
                    arr = line.split(',')
                    if arr[0] == "{'mavpackettype': 'ALTITUDE'":
                        altitude = float(arr[2].split(':')[1])
                        if curAlt < altitude:
                            curAlt = altitude
                            
                    if arr[0] == "{'mavpackettype': 'VFR_HUD'":
                        speed = float(arr[1].split(':')[1])
                        if curSpeed < speed:
                            curSpeed = speed
                                                      
                        heading = float(arr[3].split(':')[1])
                        if curHeading < heading:
                            curHeading = heading
                                                     
                        vspeed = float(arr[6].split(':')[1].strip('}'))
                        if curVSpeed < vspeed:
                            curVSpeed = vspeed
                                                   
                    if arr[0] == "{'mavpackettype': 'ATTITUDE'":
                        roll = float(arr[2].split(':')[1])
                        if curRoll < roll:
                            curRoll = roll
                                                  
                        pitch = float(arr[3].split(':')[1])
                        if curPitch < pitch:
                            curPitch = pitch
                else:
                    self.alt.append(altitude)   
                    self.speed.append(speed)  
                    self.heading.append(heading) 
                    self.vspeed.append(vspeed)
                    self.roll.append(roll)
                    self.pitch.append(pitch)
                    date = nextDate
                
    def LogPrint(self):
            print("*****Altimeter M*****")
            print(self.alt[self.iteration])

window = GUI_MainWindow()    #Main window written in pyqt5

timer = QtCore.QTimer()
time = QtCore.QTime(0, 0, 0)
timer.timeout.connect(window.timerEvent)
timer.start(1000)

timer2 = QtCore.QTimer()
timer2.timeout.connect(window.setViewWidget)
timer2.start(1000)
window.show()