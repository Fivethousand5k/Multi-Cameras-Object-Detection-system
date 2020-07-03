import threading
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QBrush, QColor, QPainter, QPixmap, QPalette, QFont, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, \
    QFileDialog
from PyQt5 import QtCore
import sys
from VideoPlayer import Player
from Online_cam_addresses import cams



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
        self.top_layout=QtWidgets.QGridLayout()
        self.top_widget.setLayout(self.top_layout)

        #顶部的3个部件： 标题，最小化按钮，关闭按钮
        self.label_title=QLabel("")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setFont(QFont("Microsoft YaHei",20,QFont.Bold))
        self.label_title.setText(u"多 路 摄 像 头 安 全 帽 检 测 系 统")
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.white)
        self.label_title.setPalette(pe)



        self.btn_close = QtWidgets.QToolButton()  # 关闭按钮
        self.btn_mini = QtWidgets.QToolButton()  # 最小化按钮

        self.top_layout.addWidget(self.label_title,0,0,1,20)
        self.top_layout.addWidget(self.btn_mini,0,20,1,1)
        self.top_layout.addWidget(self.btn_close, 0, 21, 1, 1)
        icon_btn_close = QIcon('GUI/resources/icons/main_close.png')  # 在线检测的icon
        self.btn_close.setIcon(icon_btn_close)
        self.btn_close.setIconSize(QSize(30, 30))
        self.btn_close.setStyleSheet("""
        QToolButton{border:none;color:red;}
        """)
        icon_btn_mini = QIcon('GUI/resources/icons/main_minimize.png')  # 在线检测的icon
        self.btn_mini.setIcon(icon_btn_mini)
        self.btn_mini.setIconSize(QSize(30, 30))
        self.btn_mini.setStyleSheet("""
        QToolButton{border:none;color:red;}
        """)



        self.left_widget_logoarea = QtWidgets.QWidget()  # 创建左侧部件内部的小部件，用于logo区
        self.left_widget_logoarea.setObjectName('left_widget_logoarea')


        #TOdo
        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 16)  # left_widget左上角（行号：0，列号：0） 行宽度12行 列宽度2列
        self.main_layout.addWidget(self.left_widget,1,0,12,2) # left_widget左上角（行号：0，列号：0） 行宽度12行 列宽度2列
        self.main_layout.addWidget(self.right_widget,1,2,12,14)  # right_widget左上角（行号：0，列号：0） 行宽度12行 列宽度14列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.btn_online = QtWidgets.QToolButton()
        self.btn_online.setObjectName('detection_trigger')
        icon_btn_online=QIcon('GUI/resources/icons/dome-camera4.1.png')           #在线检测的icon
        self.btn_online.setIcon(icon_btn_online)
        self.btn_online.setIconSize(QSize(120,120))
        # self.btn_online.setText("在线检测")
        # self.btn_online.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # self.btn_online.setFixedHeight(200)



        self.btn_offline = QtWidgets.QToolButton()
        self.btn_offline.setObjectName('detection_trigger')
        icon_btn_offline = QIcon('GUI/resources/icons/file4.1.png')  # 在线检测的icon
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
            border-image: url(GUI/resources/blue.jfif);
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
        self.mutex1 = threading.Lock()
        self.mutex2 = threading.Lock()
        self.mutex_list=[self.mutex1,self.mutex2]
        self.Player1 = Player(external_mutex=self.mutex1)
        self.Player2 = Player(external_mutex=self.mutex2)
        # self.Player3 = Player()
        # self.Player4 = Player()
        # self.Player5 = Player()
        # self.Player6 = Player()
        # self.Player7 = Player()
        # self.Player8 = Player()
        # self.Player9 = Player()

        self.Players_list=[self.Player1,self.Player2]


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
        self.btn_online.clicked.connect(self.online)
        self.btn_offline.clicked.connect(self.offline)
        self.btn_mini.clicked.connect(self.showMinimized)
        self.btn_close.clicked.connect(self.close)
        self.right_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.right_widget.customContextMenuRequested.connect(
            self.change_window_menu)  # 当在gBoxMain区域内点击右键时，调用用户自定义的函数 custom_right_menu

    def change_window_menu(self, pos):  # 处理在视频显示区的右键菜单显示
        menu = QMenu()
        opt1 = menu.addAction("切换到1画面")
        opt2 = menu.addAction("切换到2画面")
        opt3 = menu.addAction("切换到3画面")
        opt4 = menu.addAction("切换到4画面")
        num=1
        action = menu.exec_(self.right_widget.mapToGlobal(pos))
        if action == opt1:
            num=1
        elif action == opt2:
            num=2
        elif action == opt3:
            num=3
        elif action == opt4:
            num=4
        else:           #点击了空白处
            return
        self.change_num_of_players(num)         #切换屏幕数量

    def online(self):

        # self.btn_online.setVisible(False)
        for i in self.left_widgets:
            i.setVisible(False)
            self.left_layout.removeWidget(i)
        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(1)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['Online Cameras'])
        width,height=self.left_widget.width(),self.left_widget.height()         #获得left_widget的宽，之后使treeview的宽设为fixed
        self.tree.setFixedSize(width,height)
        self.tree.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Maximum)
        self.tree.setStyleSheet("""QTreeView {
    outline: 10px;
    background: rgb(95,158,160);
}
QTreeView::item {
    min-height: 92px;
}
QTreeView::item:hover {
    background: rgb(41, 56, 71);
}
QTreeView::item:selected {
    background: rgb(41, 56, 71);
}

QTreeView::item:selected:active{
    background: rgb(41, 56, 71);
}




    """)
        for cam in cams:
            root = QTreeWidgetItem(self.tree)
            self.tree.addTopLevelItem(root)
            root.setText(0,cam)
            root.setIcon(0, QIcon("GUI/resources/icons/camera.png"))
        self.left_layout.addWidget(self.tree,0,0,12,1)

        self.btn_return=QtWidgets.QPushButton()
        icon_btn_return = QIcon('GUI/resources/icons/return.png')  # 在线检测的icon
        self.btn_return.setIcon(icon_btn_return)
        self.btn_return.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.btn_return.setIcon(icon_btn_return)
        self.btn_return.setIconSize(QSize(40, 40))
        self.left_layout.addWidget(self.btn_return,12,0,1,1)
        self.left_widgets=[self.tree,self.btn_return]
        self.btn_return.clicked.connect(self.return_from_online)

        self.tree.itemDoubleClicked.connect(self.start_online)

    def offline(self):

        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'offline_videos')
        self.start_offline(fname)



    def start_online(self,item):
        name=item.text(0)
        address=cams[name]
        chosen_index=-1
        for id,player in enumerate(self.Players_list):
            if not player.is_working.value:    # found a unoccupied player
                chosen_index=id
                break
        if chosen_index != -1:
            player=self.Players_list[chosen_index]
            player.play_src.value=address
            player.start_online(address)
        else:                # no empty player found
            player = self.Players_list[0]

            player.restart_online(address)

    def start_offline(self,address):
        chosen_index = -1
        for id, player in enumerate(self.Players_list):
            if not player.is_working.value:  # found a unoccupied player
                chosen_index = id
                break
        if chosen_index != -1:
            player = self.Players_list[chosen_index]
            player.play_src.value = address
            player.start_offline(address)
        else:  # no empty player found
            player = self.Players_list[0]
            player.restart_offline(address)


    def close(self):
        exit()

    def return_from_online(self):
        for i in self.left_widgets:             #delete all the left_widgets and then replace them with new ones
            i.setVisible(False)
            self.left_layout.removeWidget(i)
        self.left_layout.addWidget(self.left_widget_logoarea, 0, 0, 8, 1)
        self.left_layout.addWidget(self.btn_online, 8, 0, 2, 1)
        self.left_layout.addWidget(self.btn_offline, 10, 0, 2, 1)
        self.left_widget_logoarea.setVisible(True)
        self.btn_online.setVisible(True)
        self.btn_offline.setVisible(True)
        self.left_widgets = [self.left_widget_logoarea, self.btn_online, self.btn_offline]


    def change_num_of_players(self,num):
        for i,player in enumerate(self.Players_list):   #i start with 0
            if i+1 <= num:
                pass
                player.play()
                player.setVisible(True)
            else:
                player.pause()
                player.setVisible(False)





    #下面三个函数用于实现界面拖拽
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))




def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()