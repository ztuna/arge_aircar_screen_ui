from PyQt5 import QtCore, QtGui, QtWidgets

from midScreen import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.show_1("1")
        elif event.key() ==QtCore.Qt.Key_Q:
            self.show_1("10")
        elif event.key() ==QtCore.Qt.Key_A:
            self.show_1("100")
        elif event.key() ==QtCore.Qt.Key_2:
            self.show_2("2")
        elif event.key() ==QtCore.Qt.Key_W:
            self.show_2("20")
        elif event.key() ==QtCore.Qt.Key_S:
            self.show_2("200")
        elif event.key() ==QtCore.Qt.Key_3:
            self.show_3("3")
        elif event.key() ==QtCore.Qt.Key_E:
            self.show_3("30")
        elif event.key() ==QtCore.Qt.Key_D:
            self.show_3("300")
        elif event.key() ==QtCore.Qt.Key_4:
            self.show_4("4")
        elif event.key() ==QtCore.Qt.Key_R:
            self.show_4("40")
        elif event.key() ==QtCore.Qt.Key_F:
            self.show_4("400")
        elif event.key() ==QtCore.Qt.Key_5:
            self.show_5("5")
        elif event.key() ==QtCore.Qt.Key_T:
            self.show_5("50")
        elif event.key() ==QtCore.Qt.Key_G:
            self.show_5("500")
        elif event.key() ==QtCore.Qt.Key_6:
            self.show_6("6")
        elif event.key() == QtCore.Qt.Key_0:
            self.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
