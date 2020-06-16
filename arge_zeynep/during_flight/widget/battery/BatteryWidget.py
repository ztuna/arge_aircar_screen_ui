from __future__ import division

import os
import math

from PyQt5.QtGui import QTransform
from PyQt5.QtCore import pyqtSignal, QPointF, Qt
from PyQt5  import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem

from widget.battery import qfi_rc

class Battery(QGraphicsView):
    
    viewUpdate = pyqtSignal()

    def __init__(self,winParent):
        QGraphicsView.__init__(self)
        self.winParent=winParent
        self.viewUpdate.connect(self.update)
        
        self.m_currentValue = 0
        
        self.m_scaleX = 0
        self.m_scaleY = 0
        
        self.m_originalHeight = 245
        self.m_originalWidth = 245
    
        self.m_originalCtr = QPointF(120,120)   
        
        self.m_faceZ = -20
        self.m_caseZ = 10   
        self.m_markZ = -30
        self.m_mark2Z = -30
        self.m_mark3Z = -30
        self.m_mark4Z = -30
        self.m_mark5Z = -30
        
        self.m_itemFace = None
        self.m_itemCase = None 
        self.m_itemMark = None
        self.m_itemMark2 = None
        self.m_itemMark3 = None
        self.m_itemMark4 = None
        self.m_itemMark5 = None
        
        self.setStyleSheet("background: transparent; border: none");
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setInteractive(False)
        self.setEnabled(False)

        self.m_scene = QGraphicsScene(self)
        self.setScene(self.m_scene)
        self.init()
        
    def init (self):
        os.chdir('/Users/zeyneptuna/Desktop/during_flight/widget/battery')
        
        self.m_scaleX = self.width() / self.m_originalWidth
        self.m_scaleY = self.height() / self.m_originalHeight
    
        self.m_itemFace = QGraphicsSvgItem("battery_face.svg")
        self.m_itemFace.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemFace.setZValue(self.m_faceZ)
        self.m_itemFace.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        self.m_itemFace.setTransformOriginPoint(self.m_originalCtr)
        self.m_scene.addItem(self.m_itemFace)
    
        self.m_itemCase = QGraphicsSvgItem("battery_case.svg")        
        self.m_itemCase.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemCase.setZValue(self.m_caseZ)
        self.m_itemCase.setTransform(QTransform.fromScale(self.m_scaleX, self.m_scaleY), True)
        self.m_itemCase.setTransformOriginPoint(self.m_originalCtr)
        self.m_scene.addItem(self.m_itemCase)
        
        self.m_itemMark = QGraphicsSvgItem("battery_mark.svg")
        self.m_itemMark.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemMark.setZValue(self.m_markZ)
        self.m_itemMark.setPos(57, 120)
        self.m_itemMark.setScale(0.77)
        self.m_scene.addItem(self.m_itemMark)   
        
        self.m_itemMark2 = QGraphicsSvgItem("battery_mark.svg")
        self.m_itemMark2.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemMark2.setZValue(self.m_mark2Z)
        self.m_itemMark2.setPos(57, 92.5)
        self.m_itemMark2.setScale(0.77)
        self.m_scene.addItem(self.m_itemMark2)     
        
        self.m_itemMark3 = QGraphicsSvgItem("battery_mark.svg")
        self.m_itemMark3.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemMark3.setZValue(self.m_mark3Z)
        self.m_itemMark3.setPos(57, 65)
        self.m_itemMark3.setScale(0.77)
        self.m_scene.addItem(self.m_itemMark3)
        
        self.m_itemMark4 = QGraphicsSvgItem("battery_mark.svg")
        self.m_itemMark4.setCacheMode(QGraphicsItem.NoCache)
        self.m_itemMark4.setZValue(self.m_mark4Z)
        self.m_itemMark4.setPos(57, 37.5)
        self.m_itemMark4.setScale(0.77)
        self.m_scene.addItem(self.m_itemMark4)
        
        self.m_itemMark5 = QGraphicsSvgItem("battery_mark.svg")
        self.m_itemMark5.setCacheMode (QGraphicsItem.NoCache)
        self.m_itemMark5.setZValue(self.m_mark5Z)
        self.m_itemMark5.setPos(57, 10)
        self.m_itemMark5.setScale(0.77)
        self.m_scene.addItem(self.m_itemMark5)        
        
        self.centerOn(self.width()/2, self.height()/2)
        self.updateView()
        
    def reinit(self):
        if (self.m_scene):
            self.m_scene.clear()
            self.init()

    def update(self):
        self.updateView()
        
    def setCurrentVal(self, val):
        self.m_currentValue = val
        
    def resizeEvent (self, event):
        QGraphicsView.resizeEvent (self,event)
        self.reinit()

    def reset (self):
        self.m_itemFace = None
        self.m_itemCase = None
        self.m_itemMark = None
        self.m_itemMark2 = None
        self.m_itemMark3 = None
        self.m_itemMark4 = None        
        self.m_itemMark5 = None        
        
        self.m_currentValue =  0
    
    def updateView(self):        
        if self.m_currentValue <= 20:
            self.m_itemMark2.setZValue(-30)
            
        elif self.m_currentValue <= 40:
            self.m_itemMark3.setZValue(-30)
            
        elif self.m_currentValue <= 60: 
            self.m_itemMark4.setZValue(-30)
            
        elif self.m_currentValue <= 80:  
            self.m_itemMark5.setZValue(-30)
            
        elif self.m_currentValue <= 100:
            self.m_itemMark.setZValue(20)
            self.m_itemMark2.setZValue(20)
            self.m_itemMark3.setZValue(20)
            self.m_itemMark4.setZValue(20)
            self.m_itemMark5.setZValue(20)
            
            self.m_scene.update()

