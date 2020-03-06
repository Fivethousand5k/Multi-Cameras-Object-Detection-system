from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QPainter, QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem, QLabel, QSizePolicy
from PyQt5 import QtCore
import sys
import qtawesome

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1300,800)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_widget1 = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget1.setObjectName('left_widget1')




        # self.left_label_1 = QtWidgets.QPushButton("每日推荐")
        # self.left_label_1.setObjectName('left_label')
        # self.left_label_2 = QtWidgets.QPushButton("我的音乐")
        # self.left_label_2.setObjectName('left_label')
        # self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        # self.left_label_3.setObjectName('left_label')


        #TOdo
        self.main_layout.addWidget(self.left_widget,0,0,12,2) # left_widget左上角（行号：0，列号：0） 行宽度12行 列宽度2列
        self.main_layout.addWidget(self.right_widget,0,2,12,14)  # right_widget左上角（行号：0，列号：0） 行宽度12行 列宽度14列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.btn_online = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "在线检测")
        self.btn_online.setObjectName('detection_trigger')
        self.btn_offline = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "离线检测")
        self.btn_offline.setObjectName('detection_trigger')
        self.btn1 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "离线检测")
        self.btn1.setObjectName('detection_trigger')
        self.left_layout.addWidget(self.btn1, 0, 0, 5, 1)
        self.left_layout.addWidget(self.btn_online, 5, 0, 3, 1)
        self.left_layout.addWidget(self.btn_offline, 8, 0, 3, 1)
        # #



        # TODO 关于QSizePolicy的参数介绍：  https://blog.csdn.net/qq_32417149/article/details/88398455?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
        self.btn1.setSizePolicy(QSizePolicy.ExpandFlag, QSizePolicy.Expanding)
        self.btn_offline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_online.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)







        # self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        # self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        # self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        # self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        # self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        # self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        # self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        # self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # self.setWindowOpacity(0.5)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet('''
            QWidget#left_widget{
    background:rgba(255, 255, 224, 70%);
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
        ''')
#         background: rgba(255, 100, 224, 30 %);

        self.main_widget.setStyleSheet('''
                    QWidget#main_widget{
            border-image: url(GUI/resources/factory.jpg);
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:20px;
            border-bottom-left-radius:20px;
             border-top-right-radius:20px;
            border-bottom-right-radius:20px;
        }
                ''')


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()