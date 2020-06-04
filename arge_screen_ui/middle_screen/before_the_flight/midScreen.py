# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import os
import functools
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebChannel, QtWebEngineWidgets
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent 
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtMultimedia as M
from PyQt5.QtCore import Qt, QUrl

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setContentsMargins(0,0,0,0)
        MainWindow.showFullScreen()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.photo.setText("")
        self.photo.setContentsMargins(0,0,0,0)
        self.photo.setPixmap(QtGui.QPixmap("image/start.jpg"))
        self.photo.setContentsMargins(0,0,0,0)
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
 
        self.mediaPlayer= QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videowidget = QVideoWidget(self.centralwidget)
        self.videowidget.setGeometry(QtCore.QRect(0, 0, 0, 0))

        
      


        MainWindow.setCentralWidget(self.centralwidget)


        MainWindow.setContentsMargins(0,0,0,0)
        self.retranslateUi(MainWindow)
       # QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
 
    def imageSetting(self,imageName):
        self.resetSetting()
        self.photo.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.photo.setPixmap(QtGui.QPixmap(imageName))
        

    def soundSetting(self,soundName):
        self.sound_filename = soundName
        self.sound_fullpath = QtCore.QDir.current().absoluteFilePath(self.sound_filename)
        self.sound_url      = QtCore.QUrl.fromLocalFile(self.sound_fullpath)
        self.sound_content  = M.QMediaContent(self.sound_url)
        self.sound_player   = M.QMediaPlayer()
        self.sound_player.setMedia(self.sound_content)
        self.sound_player.play()
    
    def videoSetting(self,videoName):
        self.video_filename = os.path.abspath(videoName) 
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_filename)))
        self.mediaPlayer.setVideoOutput(self.videowidget)
        self.resetSetting()
        self.videowidget.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.mediaPlayer.play()
        
    def resetSetting(self):
        self.videowidget.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.photo.setGeometry(QtCore.QRect(0, 0, 0, 0))
         

    def show_1(self,value):
        if value == "1":
           self.imageSetting("image/1.png")
        elif value == "10":
           self.imageSetting("image/1n.png")
        elif value == "100":
           self.imageSetting("image/1y.png")
           self.soundSetting('sound/1.mp3')

    def show_2(self,value):
        if value == "2":
           self.imageSetting("image/2.png")
        elif value == "20":
           self.imageSetting("image/2n.png")
           self.soundSetting("sound/2.mp3")
        elif value == "200":
           self.videoSetting('video/2y.mp4')

    def show_3(self,value):
        if value == "3":
           self.imageSetting("image/3.png")
        elif value == "30":
           self.imageSetting("image/3n.png")
           self.soundSetting("sound/3.mp3")
        elif value == "300":
           self.videoSetting('video/3y.mp4')

    def show_4(self,value):
        if value == "4":
           self.imageSetting("image/4.png")
        elif value == "40":
           self.soundSetting("sound/4.mp3")
           self.imageSetting("image/4n.png")
        elif value == "400":
           self.imageSetting('image/5.png')
           self.soundSetting("sound/5.mp3")

    def show_5(self,value):
        if value == "5":
           self.imageSetting("image/5.png")
           self.soundSetting("sound/5.mp3")
        elif value == "50":
           self.imageSetting("image/6.png")
        elif value == "500":
           self.soundSetting("music/1.mp3")
           self.imageSetting("image/6.png")

    def show_6(self,value):
        if value == "6":
           self.imageSetting("image/6.png")

    
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
