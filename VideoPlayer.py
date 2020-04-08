import cv2
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtCore
from MyDetector import Helmet_Detector
import threading
from torch.multiprocessing import Process
import  torch.multiprocessing as mp

import  time
import  datetime
from Processor import detector,play



class Player(QWidget):
    def __init__(self,parent=None):
        super(Player, self).__init__(parent)
        self.init_UI()
        self.init_process()
        self.init_offline()

    def init_UI(self):
        self.layout1=QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.label_screen = QtWidgets.QLabel(self)  # 用于展示图片的label
        self.btn_start = QtWidgets.QToolButton()
        self.btn_pause = QtWidgets.QToolButton()
        self.btn_close = QtWidgets.QToolButton()
        self.label_info= QtWidgets.QLabel()
        self.progressBar = QtWidgets.QSlider()
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.layout1.addWidget(self.label_info,0,0,1,7)
        self.layout1.addWidget(self.btn_close, 0, 7, 1, 1)
        self.layout1.addWidget(self.label_screen, 1, 0, 7, 8)
        self.layout1.addWidget(self.btn_start, 8, 0, 1, 1)
        self.layout1.addWidget(self.btn_pause, 8, 1, 1, 1)
        self.layout1.addWidget(self.progressBar, 8, 2, 1, 6)

        # self.label_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_screen.setScaledContents(True)
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        self.setLayout(self.layout1)  # 设置窗口主部件布局为网格布局



    def init_process(self):
        self.origin_img_q=mp.Queue(maxsize=2)
        self.result_img_q=mp.Queue(maxsize=4)
        self.p_detector = Process(target=detector,args = (self.origin_img_q,self.result_img_q))
        self.p_detector.start()
        self.img_fetcher=Process(target=play,args = (self.origin_img_q,))
        self.img_fetcher.start()

    def display(self):
        while True:
            if not self.result_img_q.empty():
                prev = time.time()
                show=self.result_img_q.get()
                post = time.time()

                showImage = QImage(show.data, show.shape[1], show.shape[0],
                                   QImage.Format_RGB888)  # 转换成QImage类型
                self.label_screen.setScaledContents(True)

                self.label_screen.setPixmap(QPixmap.fromImage(showImage))  #







    def init_offline(self,video_path=None):
        """

        :param video_path:  要离线播放的video地址
        :return:
        """
        self.timer = QTimer(self)           #计时器，用于以线程方式定时唤醒播放

        self.offline_video_thread = threading.Thread(target=self.display)
        self.offline_video_thread.start()






