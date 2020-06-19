from __future__ import division

import math
import os

from PyQt5.QtGui import QTransform
from PyQt5.QtCore import pyqtSignal, QPointF, Qt
from PyQt5  import QtCore
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem

from widget.flight_duration import qfi_rc

class fDuration (QGraphicsView):

    viewUpdate = pyqtSignal()

    def __init__(self,winParent):
        QGraphicsView.__init__(self)
        self.winParent=winParent
        self.viewUpdate.connect(self.update)
        
        self.m_hour = 0
        self.m_min = 0
        self.m_sec = 0        

        self.m_scaleX = 0
        self.m_scaleY = 0

        self.m_originalHeight = 245
        self.m_originalWidth = 245

        self.m_originalFdCtr = QPointF(120,120)
        self.m_originalMarkCtr = QPointF(120, 120)        

        self.m_faceZ = -20
        self.m_handZ = -10
        self.m_caseZ = 10
        self.m_mark1Z = 20
        self.m_mark2Z = 30
        self.m_mark3Z = 40       

        self.m_itemHand = None
        self.m_itemFace = None
        self.m_itemCase = None
        self.m_itemMark1 = None
        self.m_itemMark2 = None
        self.m_itemMark3 = None

        self.setStyleSheet("background: transparent; border: none");
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setInteractive(False)
        self.setEnabled(False)

        self.m_scene = QGraphicsScene(self)
        self.setScene(self.m_scene)
        self.init()

    def init (self):
        #os.chdir('/Users/zeyneptuna/Desktop/during_flight/widget/flight_duration')
        
        self.m_scaleX = self.width() / self.m_originalWidth
        self.m_scaleY = self.height() / self.m_originalHeight
                
        self.m_itemFace = QGraphicsSvgItem("widget/flight_duration/fd_face.svg")
        self.m_itemFace.setCacheMode(QGraphicsItem.NoCache)
        self.m_itemFace.setZValue(self.m_faceZ)
        self.m_itemFace.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        self.m_itemFace.setTransformOriginPoint(self.m_originalFdCtr)
        self.m_scene.addItem(self.m_itemFace)

        self.m_itemCase = QGraphicsSvgItem("widget/flight_duration/fd_case.svg")        
        self.m_itemCase.setCacheMode(QGraphicsItem.NoCache)
        self.m_itemCase.setZValue(self.m_caseZ)
        self.m_itemCase.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        self.m_itemCase.setTransformOriginPoint(self.m_originalFdCtr)
        self.m_scene.addItem(self.m_itemCase)
        
        #self.m_itemMark1 = QGraphicsSvgItem("fd_mark_1.svg")        
        #self.m_itemMark1.setCacheMode(QGraphicsItem.NoCache)
        #self.m_itemMark1.setZValue(self.m_mark1Z)
        #self.m_itemMark1.setTransformOriginPoint(self.m_originalMarkCtr)
        #self.m_itemMark1.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        #self.m_scene.addItem(self.m_itemMark1)       
        
        #self.m_itemMark2 = QGraphicsSvgItem("fd_mark_2.svg")        
        #self.m_itemMark2.setCacheMode(QGraphicsItem.NoCache)
        #self.m_itemMark2.setZValue(self.m_mark2Z)
        #self.m_itemMark2.setTransformOriginPoint(self.m_originalMarkCtr)
        #self.m_itemMark2.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        #self.m_scene.addItem(self.m_itemMark2)        
        
        #self.m_itemMark3 = QGraphicsSvgItem("fd_mark_3.svg")               
        #self.m_itemMark3.setCacheMode(QGraphicsItem.NoCache)
        #self.m_itemMark3.setZValue(self.m_mark3Z)
        #self.m_itemMark3.setTransformOriginPoint(self.m_originalMarkCtr)
        #self.m_itemMark3.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        #self.m_scene.addItem(self.m_itemMark3)                

        self.centerOn (self.width()/2, self.height()/2)
        self.updateView()

    def reinit(self):
        if (self.m_scene):
            self.m_scene.clear()
            self.init()

    def update(self):
        self.updateView()

    def setHour (self, hour):
        self.m_hour = hour
        
    def setMin (self, mins):
        self.m_min = mins    
        
    def setSec (self, sec):
        self.m_sec = sec   

    def resizeEvent (self, event):
        QGraphicsView.resizeEvent (self,event)
        self.reinit()

    def reset (self):
        self.m_itemFace = None
        self.m_itemCase = None
        self.m_itemMark1 = None
        self.m_itemMark2 = None
        self.m_itemMark3 = None        

        self.m_hour =  0
        self.m_min = 0
        self.m_sec = 0

    def updateView(self):
            
        #angle1 = 90*((self.m_hour - 9)/3)
        #angle2 = 90*((self.m_min)/15)        
        #angle3 = 90*((self.m_sec - 54)/15)

        #self.m_itemMark1.setRotation( angle1 )
        #self.m_itemMark2.setRotation( angle2 )
        #self.m_itemMark3.setRotation( angle3 )

        self.m_scene.update()
