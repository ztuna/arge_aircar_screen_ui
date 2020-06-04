

from PyQt5 import QtCore, QtGui, QtWidgets, QtQml, QtQuick, QtQuickWidgets, QtWebChannel, QtWebEngineWidgets

class BatteryWidget(QtCore.QObject):
    currentValueChanged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(BatteryWidget, self).__init__(parent)
        self.rev=100
        self.m_currentValue = 0

    @QtCore.pyqtProperty(float, notify=currentValueChanged)
    def currentValue(self):
        return self.m_currentValue

    @currentValue.setter
    def currentValue(self, v):
        if self.m_currentValue == v:
            return
        self.m_currentValue = v
        self.currentValueChanged.emit(v)

    def current_value(self):
        self.rev-=1
        if self.rev <0:
           self.rev=100
        self.currentValue = self.rev

