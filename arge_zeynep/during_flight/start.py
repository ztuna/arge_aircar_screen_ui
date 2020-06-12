import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtQml, QtQuick, QtQuickWidgets, QtWebChannel, QtWebEngineWidgets

from widget.battery.RadialBar import RadialBar
from widget.battery.BatteryWidget import BatteryWidget

class Ui_MainWindow(object):
    
    def openWindow(self):
        from main_nighttime import GUI_MainWindow
        window.hide()
  
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        MainWindow.resize(screenSize.width(), screenSize.height())   
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)        
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(screenSize.width()/2.3 , screenSize.height()/2.2, 150, 60))
        self.pushButton.setObjectName("pushButton")
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        MainWindow.showFullScreen()
        self.pushButton.clicked.connect(self.openWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        
        dir_ = QtCore.QDir("Roboto_Slab")
        _id = QtGui.QFontDatabase.addApplicationFont("Roboto_Slab/RobotoSlab-SemiBold.ttf")   
        font = QtGui.QFont("Roboto Slab")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        
        self.pushButton.setText(_translate("MainWindow", "Uçuşu başlat"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Flight Indicators"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

