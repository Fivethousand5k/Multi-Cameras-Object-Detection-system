import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QSizePolicy

import threading
import  time



class Player(QWidget):
    def __init__(self,mutex,parent=None,):
        super(Player, self).__init__(parent)
        self.play_mutex=mutex
        self.init_UI()
        self.init_data()
        # self.init_process()
        self.init_connect()
        # self.init_offline()


    def init_UI(self):
        self.layout1=QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.label_screen = QtWidgets.QLabel(self)  # 用于展示图片的label
        self.btn_start = QtWidgets.QToolButton()
        self.btn_pause = QtWidgets.QToolButton()
        self.btn_close = QtWidgets.QToolButton()
        self.btn_start.setIcon(QIcon('GUI/resources/icons/play.png'))
        self.btn_start.setIconSize(QSize(30, 30))
        self.btn_pause.setIcon(QIcon('GUI/resources/icons/pause.png'))
        self.btn_pause.setIconSize(QSize(30, 30))
        self.btn_close.setIcon(QIcon('GUI/resources/icons/close.png'))
        self.btn_close.setIconSize(QSize(30, 30))

        self.setStyleSheet('''
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

        self.label_info= QtWidgets.QLabel()
        self.label_info.setText("[空闲]")
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.white)
        self.label_info.setPalette(pe)
        self.label_info.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.progressBar = QtWidgets.QSlider()
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.layout1.addWidget(self.label_info,0,0,1,7)
        self.layout1.addWidget(self.btn_close, 0, 7, 1, 1)
        self.layout1.addWidget(self.label_screen, 1, 0, 7, 8)
        self.layout1.addWidget(self.btn_start, 8, 0, 1, 1)
        self.layout1.addWidget(self.btn_pause, 8, 1, 1, 1)
        self.layout1.addWidget(self.progressBar, 8, 2, 1, 6)
        self.bottom_widgets=[self.btn_start,self.btn_pause,self.progressBar]
        # self.label_screen.setScaledContents(True)
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        self.setLayout(self.layout1)  # 设置窗口主部件布局为网格布局


    def init_data(self):
        self.is_working=False
        self.semaphore=True
        self.running=True

        self.mutex = threading.Lock()
        self.frame_total=0    # the num of frames in a selected video,used for updating the max-num of slider
        self.frame_index=0    # current position of slider

        self.timer = QTimer(self)  # used for the updating of progress bar
        self.temp_timer=QTimer(self)  #used for detecting whether the frame_total is given.

        self.mode = None                # 'online' or 'offline'

    def init_connect(self):
        self.btn_pause.clicked.connect(self.pause)
        self.btn_close.clicked.connect(self.close)
        self.btn_start.clicked.connect(self.play)
        self.progressBar.sliderPressed.connect(
            self.lockBar)  # when the user is dragging the slider, stop updating the value
        self.progressBar.sliderReleased.connect(self.change_progressBar)

    def init_offline_connect(self):

        self.timer.timeout.connect(self.update_progressBar)
        self.timer.start(50)  # update the progressbar value every 50ms
        self.temp_timer.timeout.connect(self.set_MaxValue)
        self.temp_timer.start(50)

        #progressbar
        self.progressBar.sliderPressed.connect(self.lockBar) # when the user is dragging the slider, stop updating the value
        self.progressBar.sliderReleased.connect(self.change_progressBar)

    def display(self,src):
        """

               :param src:  the path of video to be played
               :return:
               """
        self.video_src=src
        self.is_working=True
        self.label_info.setText('[离线模式]:' + src)
        self.video_thread = threading.Thread(target=self.display1)
        self.video_thread.start()
    def display1(self):

        # self.is_working=True
        # self.playing=True
        while self.running:
            if self.is_working:
                self.videocap = cv2.VideoCapture(self.video_src if self.video_src != '0' else 0)
                self.frame_total = int(self.videocap.get(7))  # 得到总帧数
                self.frame_index=0
                self.progressBar.setMaximum(self.frame_total)
                self.playing = True
            while self.is_working:     # the first while loop; when the btn_close is clicked, self.is_working would be set false
                while self.playing:        # the second while loop; when the btn_play/btn_pause is clicked,self.playing would be set true/false
                    self.mutex.acquire()
                    flag, frame = self.videocap.read()

                    if flag:  # The frame is ready and already captured
                        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                        # show = cv2.resize(frame, (int(self.label_screen.width()*0.9), int(self.label_screen.height()*0.9)),
                        #                    interpolation=cv2.INTER_AREA)
                        showImage = QImage(show, show.shape[1], show.shape[0],
                                           QImage.Format_RGB888)  # 转换成QImage类型
                        self.play_mutex.acquire()

                        self.label_screen.setPixmap(QPixmap.fromImage(showImage))  #
                        self.label_screen.setScaledContents(True)
                        self.play_mutex.release()
                        self.frame_index += 1
                        self.progressBar.setValue(self.frame_index)
                    else:
                        self.playing=False
                        self.is_working=False
                    self.mutex.release()
                    time.sleep(0.03)
                time.sleep(0.05)
            self.videocap.release()
            time.sleep(0.05)

    def lockBar(self):
        self.mutex.acquire()
    def change_progressBar(self):

        self.frame_index = self.progressBar.value()
        self.videocap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
        self.mutex.release()


    def play_new(self,src):
        self.video_src = src
        if self.is_working:
            self.playing=False
            self.is_working=False
            time.sleep(0.2)
            self.playing = True
            self.is_working = True

        else:
            self.playing = True
            self.is_working = True

        self.label_info.setText('[离线模式]:' + src)

    def Fix_Size(self,size):        #fix the size of videoplayer
        self.setFixedSize(size[0],size[1])
    def clear(self):
        self.label_screen.setPixmap(QPixmap(""))  # 移除label上的图片
    def play(self):
        self.playing=True
        temp_str = self.label_info.text()
        if '[暂停]' in temp_str:
            temp_str = temp_str.replace('[暂停]', '')
        self.label_info.setText(temp_str)
    def pause(self):
        print(11)
        self.playing=False
        temp_str = self.label_info.text()
        if '[暂停]' not in temp_str:
            temp_str = '[暂停]' + temp_str
        self.label_info.setText(temp_str)
    def close(self):
        self.playing=False
        self.is_working=False
        time.sleep(0.1)
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        self.label_info.setText('空闲')
    def terminate(self):            #used only when the whole program  shut down
        self.playing=False
        self.is_working=False
        self.running=False


