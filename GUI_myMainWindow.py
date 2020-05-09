from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QPainter, QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget
from PyQt5 import QtCore
import sys
from VideoPlayer import Player
import sip
import qtawesome


MaxNumOfVideo=9    #最大支持播放数量

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.setFixedSize(1400,900)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget(self.main_widget)  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')

        self.top_widget=QtWidgets.QWidget()  # 创建顶部部件
        self.top_widget.setObjectName('top_widget')







        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_widget_logoarea = QtWidgets.QWidget()  # 创建左侧部件内部的小部件，用于logo区
        self.left_widget_logoarea.setObjectName('left_widget_logoarea')




        #TOdo
        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 16)  # left_widget左上角（行号：0，列号：0） 行宽度12行 列宽度2列
        self.main_layout.addWidget(self.left_widget,1,0,12,2) # left_widget左上角（行号：0，列号：0） 行宽度12行 列宽度2列
        self.main_layout.addWidget(self.right_widget,1,2,12,14)  # right_widget左上角（行号：0，列号：0） 行宽度12行 列宽度14列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.btn_online = QtWidgets.QToolButton()
        self.btn_online.setObjectName('detection_trigger')
        icon_btn_online=QIcon('GUI/resources/icons/dome-camera1.9.png')           #在线检测的icon
        self.btn_online.setIcon(icon_btn_online)
        self.btn_online.setIconSize(QSize(120,120))
        # self.btn_online.setText("在线检测")
        # self.btn_online.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # self.btn_online.setFixedHeight(200)



        self.btn_offline = QtWidgets.QToolButton()
        self.btn_offline.setObjectName('detection_trigger')
        icon_btn_offline = QIcon('GUI/resources/icons/file3.1.png')  # 在线检测的icon
        self.btn_offline.setIcon(icon_btn_offline)
        self.btn_offline.setIconSize(QSize(120, 120))
        # self.btn_offline.setFixedHeight(200)
        self.btn_offline.setObjectName('detection_trigger')



        self.left_layout.addWidget(self.left_widget_logoarea, 0, 0, 8, 1)
        self.left_layout.addWidget(self.btn_online, 8, 0, 2, 1)
        self.left_layout.addWidget(self.btn_offline, 10, 0, 2, 1)
        self.left_widgets=[self.left_widget_logoarea,self.btn_online,self.btn_offline]

        # #



        # TODO 关于QSizePolicy的参数介绍：  https://blog.csdn.net/qq_32417149/article/details/88398455?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
        self.btn_offline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_online.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)




        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # self.setWindowOpacity(0.5)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明


        """
        左侧菜单栏的qss
        如果要加蒙版四周的白边，用下列代码：
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-left:1px solid white;
        """
        self.setStyleSheet('''
            QWidget#left_widget{
    background:rgba(205, 38, 38, 20%);
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
QWidget#right_widget{
    background:rgba(255, 255, 224, 20%);

    border-top-right-radius:10px;
    border-bottom-right-radius:10px;
}
'''

)
        #todo  左侧按钮qss
        self.left_widget.setStyleSheet('''
            QToolButton{border:none;color:red;}
            QToolButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QToolButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')



        self.main_widget.setStyleSheet('''
                    QWidget#main_widget{
            border-image: url(GUI/resources/yellowwhite.jfif);
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:20px;
            border-bottom-left-radius:20px;
             border-top-right-radius:20px;
            border-bottom-right-radius:20px;
        }
                ''')

        self.main_layout.setSpacing(0)


        #右侧播放界面设置
        self.right_layout = QtWidgets.QGridLayout()  # 创建右侧部件的网格布局
        self.right_layout.setSpacing(1)
        self.Player1 = Player()
        self.Player2 = Player()
        # self.Player3 = Player()
        # self.Player4 = Player()
        # self.Player5 = Player()
        # self.Player6 = Player()
        # self.Player7 = Player()
        # self.Player8 = Player()
        # self.Player9 = Player()

        # self.Players_list=[self.Player1,self.Player2,self.Player3,
        #                    self.Player4,self.Player5,self.Player6,
        #                    self.Player7,self.Player8,self.Player9]


        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格



        self.right_layout.addWidget(self.Player1,0,0)
        self.right_layout.addWidget(self.Player2, 0,1)
        # self.right_layout.addWidget(self.Player3, 1, 0)
        # self.right_layout.addWidget(self.Player4, 1, 1)
        # self.Player1.init_offline(name)
        #
        # # print(self.right_widget.size())
        # # self.Player1.setFixedSize(800,480)
        # self.right_layout.addWidget(self.Player2,0,1)
        # self.right_layout.addWidget(self.Player3,1,0)
        # self.right_layout.addWidget(self.Player4,1,1)
        # self.Player2.init_offline(name)
        # self.Player3.init_offline(name)
        # self.Player4.init_offline(name)
        # self.right_layout.addWidget(self.Player5)
        # self.right_layout.addWidget(self.Player6)
        # self.right_layout.addWidget(self.Player7)
        # self.right_layout.addWidget(self.Player8)
        # self.right_layout.addWidget(self.Player9)


        # self.vdo_widget2 = QtWidgets.QWidget()
        # self.vdo_widget3 = QtWidgets.QWidget()
        # self.vdo_widget4 = QtWidgets.QWidget()
        # self.vdo_widget5 = QtWidgets.QWidget()
        # self.vdo_widget6 = QtWidgets.QWidget()
        # self.vdo_widget7 = QtWidgets.QWidget()
        # self.vdo_widget8 = QtWidgets.QWidget()
        # self.vdo_widget9 = QtWidgets.QWidget()


    def init_connect(self):
        self.btn_online.clicked.connect(self.a)


    def a(self):
        print("asd")

        # self.btn_online.setVisible(False)
        for i in self.left_widgets:
            i.setVisible(False)
            self.left_layout.removeWidget(i)
        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.left_layout.addWidget(self.tree,0,0,1,1)



    def change_to_9_screens(self):
        for i in range(self.right_layout.count()):                        #首先清空layout内所有的widget
            self.right_layout.itemAt(i).widget().deleteLater()

        for player in self.Players_list:
            self.right_layout.addWidget(player)




def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()