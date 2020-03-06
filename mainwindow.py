
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QPainter, QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem, QLabel
from PyQt5 import QtCore
import sys

from GUI.GUI_mainwindow import Ui_Mainwindow

class Mainwindow(QtWidgets.QWidget,Ui_Mainwindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.init_UI()



    def init_UI(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("GUI/resources/factory-3.jpg").scaled(self.width(),self.height())))
        self.setPalette(palette)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setStyleSheet("border-radius:100px")


        ##todo 透明度
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Mainwindow()
    myWin.show()
    sys.exit(app.exec_())