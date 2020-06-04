import sys
import os
import csv
import functools
from random import randrange

from PyQt5 import QtCore, QtGui, QtWidgets, QtQml, QtQuick, QtQuickWidgets, QtWebChannel, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

from widget.battery.RadialBar import RadialBar
from widget.compass import CompassWidget
from widget.battery.BatteryWidget import BatteryWidget
from widget.speed import SpeedWidget
from widget.attitude import AttitudeWidget
from widget.altimeter import AltimeterWidget
from widget.variometer import VariometerWidget
from widget.turn   import TurnWidget

import random
import math



          

class GUI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.resize(1920,1080)
        self.iteration=0
        self.batterySize=100
        self.speedSize=0
        self.latVal = 0
        self.lngVal = 0
        self.LpanSize=0
        self.battery = BatteryWidget()
        self.centralwidget = QtWidgets.QWidget(self)
        self.f=open('vehicle_gps_position.csv','r')
        
          
        self.centralwidget.setObjectName("centralwidget")
        self.lat   = []
        self.lon   = []
        self.x_mag = []
        self.y_mag = []
        self.alt   = []
        self.ground_speed = []
        self.vertical_speed = []
        self.dataReader() 
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "widget/map/map.html",
        )
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(file))
        self.webView.setObjectName("webView")
  
        palette = QtGui.QPalette()
        palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))

         # 0,0
        self.attitudeLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.attitudeLayoutWidget.setGeometry(QtCore.QRect(0, 50, 200, 200))
        self.attitudeLayoutWidget.setObjectName("attitudeLayoutWidget") 
        self.attitudeLayout = QtWidgets.QGridLayout(self.attitudeLayoutWidget)
        self.attitudeLayout.setContentsMargins(0, 0, 0, 0)
        self.attitudeLayout.setObjectName("attitudeLayout")
        self.attitudeWidget = AttitudeWidget.Attitude(self.attitudeLayoutWidget)
        self.attitudeWidget.reinit()
        self.attitudeLayout.addWidget(self.attitudeWidget)
        self.attitudeLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.attitudeLcdNumber.setGeometry(QtCore.QRect(0, 250, 200, 45))
        self.attitudeLcdNumber.setDigitCount(8)
        self.attitudeLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.attitudeLcdNumber.setProperty("value", 1.0)
        self.attitudeLcdNumber.setObjectName("attitudelcdNumber")
        self.attitudeLcdNumber.setPalette(palette)

         # 1,0
        self.variometerLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.variometerLayoutWidget.setGeometry(QtCore.QRect(0, 325, 200, 200))
        self.variometerLayoutWidget.setObjectName("variometerLayoutWidget") 
        self.variometerLayout = QtWidgets.QGridLayout(self.variometerLayoutWidget)
        self.variometerLayout.setContentsMargins(0, 0, 0, 0)
        self.variometerLayout.setObjectName("variometerLayout")
        self.variometerWidget = VariometerWidget.Variometer(self.variometerLayoutWidget)
        self.variometerWidget.reinit()
        self.variometerLayout.addWidget(self.variometerWidget)
        self.variometerLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.variometerLcdNumber.setGeometry(QtCore.QRect(0, 525, 200, 45))
        self.variometerLcdNumber.setDigitCount(8)
        self.variometerLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.variometerLcdNumber.setProperty("value", 2.0)
        self.variometerLcdNumber.setObjectName("variometerlcdNumber")
        self.variometerLcdNumber.setPalette(palette)


        # 2,0
        self.turnLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.turnLayoutWidget.setGeometry(QtCore.QRect(0, 595, 200, 200))
        self.turnLayoutWidget.setObjectName("turnLayoutWidget") 
        self.turnLayout = QtWidgets.QGridLayout(self.turnLayoutWidget)
        self.turnLayout.setContentsMargins(0, 0, 0, 0)
        self.turnLayout.setObjectName("turnLayout")
        self.turnWidget = TurnWidget.Turn(self.turnLayoutWidget)
        self.turnWidget.reinit()
        self.turnLayout.addWidget(self.turnWidget)
        self.turnLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.turnLcdNumber.setGeometry(QtCore.QRect(0, 795, 200, 45))
        self.turnLcdNumber.setDigitCount(8)
        self.turnLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.turnLcdNumber.setProperty("value", 3.0)
        self.turnLcdNumber.setObjectName("variometerlcdNumber")
        self.turnLcdNumber.setPalette(palette)
                
        # 0,1
        self.compassLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.compassLayoutWidget.setGeometry(QtCore.QRect(1720, 50, 200, 200))
        self.compassLayoutWidget.setObjectName("compassLayoutWidget") 
        self.compassLayout = QtWidgets.QGridLayout(self.compassLayoutWidget)
        self.compassLayout.setContentsMargins(0, 0, 0, 0)
        self.compassLayout.setObjectName("compassLayout")
        self.compassWidget = CompassWidget.qfi_HSI(self.compassLayoutWidget)
        self.compassWidget.reinit()
        self.compassLayout.addWidget(self.compassWidget)        
        self.compassLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.compassLcdNumber.setGeometry(QtCore.QRect(1720, 250, 200, 45))
        self.compassLcdNumber.setDigitCount(8)
        self.compassLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.compassLcdNumber.setProperty("value", 4.0)
        self.compassLcdNumber.setObjectName("compasslcdNumber")
        self.compassLcdNumber.setPalette(palette)
 
        # 1,1
        self.speedLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.speedLayoutWidget.setGeometry(QtCore.QRect(1720, 325, 200, 200))
        self.speedLayoutWidget.setObjectName("speedLayoutWidget") 
        self.speedLayout = QtWidgets.QGridLayout(self.speedLayoutWidget)
        self.speedLayout.setContentsMargins(0, 0, 0, 0)
        self.speedLayout.setObjectName("speedLayout")
        self.speedWidget = SpeedWidget.qfi_SI(self.speedLayoutWidget)
        self.speedWidget.reinit()
        self.speedLayout.addWidget(self.speedWidget)
        self.speedLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.speedLcdNumber.setGeometry(QtCore.QRect(1720, 525, 200, 45))
        self.speedLcdNumber.setDigitCount(8)
        self.speedLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.speedLcdNumber.setProperty("value", 5.0)
        self.speedLcdNumber.setObjectName("speedlcdNumber")
        self.speedLcdNumber.setPalette(palette)

        #2,1
        self.altLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.altLayoutWidget.setGeometry(QtCore.QRect(1720, 595, 200, 200))
        self.altLayoutWidget.setObjectName("altLayoutWidget") 
        self.altLayout = QtWidgets.QGridLayout(self.altLayoutWidget)
        self.altLayout.setContentsMargins(0, 0, 0, 0)
        self.altLayout.setObjectName("altLayout")
        self.altimeterWidget = AltimeterWidget.Altimeter(self.altLayoutWidget)
        self.altimeterWidget.reinit()
        self.altLayout.addWidget(self.altimeterWidget)
        self.altLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.altLcdNumber.setGeometry(QtCore.QRect(1720, 795, 200, 45))
        self.altLcdNumber.setDigitCount(8)
        self.altLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.altLcdNumber.setProperty("value", 6.0)
        self.altLcdNumber.setObjectName("altlcdNumber")
        self.altLcdNumber.setPalette(palette)

        #3,1
        self.batteryCWidget = QtQuickWidgets.QQuickWidget(self.centralwidget)
        self.batteryCWidget.setGeometry(QtCore.QRect(1750,890,200,200))
        self.batteryLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.batteryLcdNumber.setGeometry(QtCore.QRect(1720, 1035, 200, 45))
        self.batteryLcdNumber.setDigitCount(8)
        self.batteryLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.batteryLcdNumber.setProperty("value", 1000.0)
        self.batteryLcdNumber.setObjectName("batterylcdNumber")
        self.batteryLcdNumber.setPalette(palette)


        

      #  self.compassWidget = CompassWidget(self.centralwidget)
       # self.compassWidget.setGeometry(QtCore.QRect(1760,200,150,150))
       # self.compassLcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
       # self.compassLcdNumber.setGeometry(QtCore.QRect(1720, 355, 200, 45))
       # self.compassLcdNumber.setDigitCount(8)
       # self.compassLcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
       # self.compassLcdNumber.setProperty("value", 1000.0)
       # self.compassLcdNumber.setObjectName("compasslcdNumber")
       # self.compassLcdNumber.setPalette(palette)        


        self.setCentralWidget(self.centralwidget)

        self.showFullScreen()
    
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
    
    def speedCalculate(self):
        speed = math.sqrt( (self.lon[self.iteration]-self.lon[self.iteration-1])**2 + (self.lat[self.iteration]-self.lat[self.iteration-1])**2  )
        return speed

    def setViewWidget(self):
        self.iteration+=1
        self.speedSize+=1
        self.batterySize-=1
        if self.batterySize < 0:
           self.batterySize=100
        if self.speedSize > 16:
           self.speedSize = 0

        self.panMap(self.lon[self.iteration],self.lat[self.iteration])
        self.compassWidget.setHeading(30)
        self.speedWidget.setSpeed(12)        
        self.altimeterWidget.setAltitude(self.alt[self.iteration])
        self.attitudeWidget.setRoll(10*math.cos(45))
        self.attitudeWidget.setPitch(10*math.cos(45))
        self.variometerWidget.setClimbRate(100)
        self.turnWidget.setTurnRate(10*math.cos(45))
        self.turnWidget.setSlipSkid(10*math.cos(45))
                
        self.compassWidget.viewUpdate.emit()
        self.speedWidget.viewUpdate.emit()
        self.altimeterWidget.viewUpdate.emit()
        self.attitudeWidget.viewUpdate.emit()
        self.variometerWidget.viewUpdate.emit()
        self.turnWidget.viewUpdate.emit()

       # self.compassLcdNumber.setProperty("value", self.compassWidget.compassDegCalculate(float(self.x_mag[self.iteration]),float(self.y_mag[self.iteration])))
        self.attitudeLcdNumber.setProperty("value","45")
        self.speedLcdNumber.setProperty("value",12)
        self.batteryLcdNumber.setProperty("value", self.batterySize)
        self.altLcdNumber.setProperty("value", self.alt[self.iteration])
        self.variometerLcdNumber.setProperty("value", 100)
        self.turnLcdNumber.setProperty("value", 10*math.cos(45))
        self.compassLcdNumber.setProperty("value", 30)
        

        self.LogPrint()



    def panMap(self, lng, lat):
        page = self.webView.page()
        self.LpanSize+=1
        page.runJavaScript('items.push([{},{}]);'.format(lat,lng)) 
        page.runJavaScript("if(items.length>2) Enditems.push([items[items.length-3][0],items[items.length-3][1]],[items[items.length-2][0],items[items.length-2][1]]);")
        
        page.runJavaScript("polyline = L.polyline(Enditems, {color: 'blue'}).addTo(map);")
        page.runJavaScript("map.panTo(L.latLng({}, {}));".format(lat, lng))
        self.IconCalculate(lat,lng)
        page.runJavaScript("marker.setLatLng(map.getCenter());")
        page.runJavaScript("Enditems = [];")    
        
    
    def IconCalculate(self,lat,lng):
         page = self.webView.page()
         if lat == self.latVal and lng < self.lngVal:
            page.runJavaScript("marker.setIcon(aircarIconL);")
            self.latVal = lat
            self.lngVal = lng
         elif lat == self.latVal and lng > self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconR);")
              self.latVal = lat
              self.lngVal = lng
         elif lat > self.latVal and lng == self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconU);")
              self.latVal = lat
              self.lngVal = lng
         elif lat < self.latVal and lng == self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconD);")
              self.latVal = lat
              self.lngVal = lng
         elif lat > self.latVal and lng < self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconUL);")
              self.latVal = lat
              self.lngVal = lng
         elif lat > self.latVal and lng > self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconUR);")
              self.latVal = lat
              self.lngVal = lng
         elif lat < self.latVal and lng < self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconDL);")
              self.latVal = lat
              self.lngVal = lng
         elif lat < self.latVal and lng > self.lngVal:
              page.runJavaScript("marker.setIcon(aircarIconDR);")
              self.latVal = lat
              self.lngVal = lng

   



#app = QtWidgets.QApplication(sys.argv)
window = GUI_MainWindow()    #Main window written in pyqt5

    #Battery Widget
QtQml.qmlRegisterType(RadialBar, "SDK", 1,0, "RadialBar")
batteryWidget = BatteryWidget() # Class with function to update data in QML
context = window.batteryCWidget.rootContext()
context.setContextProperty("batteryWidget",batteryWidget)
window.batteryCWidget.setSource(QtCore.QUrl.fromLocalFile('widget/battery/qml_widget.qml'))


timer = QtCore.QTimer() 
timer.timeout.connect(batteryWidget.current_value)
timer.start(1000)
timer2 = QtCore.QTimer()
timer2.timeout.connect(window.setViewWidget)
timer2.start(200)
window.show()
#sys.exit(app.exec_())

