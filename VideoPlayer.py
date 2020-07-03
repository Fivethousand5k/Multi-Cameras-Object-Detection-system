from ctypes import c_bool

import cv2
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtCore
from MyDetector import Helmet_Detector
from ctypes import c_char_p
import threading
from torch.multiprocessing import Process,Value,Lock,Manager
import  torch.multiprocessing as mp

import  time
import  datetime
from Processor import detector,play



class Player(QWidget):
    def __init__(self,external_mutex,parent=None):
        super(Player, self).__init__(parent)
        self.init_UI()
        self.init_data()
        self.init_process()
        self.init_connect()
        self.init_offline()
        self.external_mutex=external_mutex

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
        self.label_screen.setScaledContents(True)
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        self.setLayout(self.layout1)  # 设置窗口主部件布局为网格布局


    def init_data(self):
        self.is_working=False
        self.semaphore=True
        self.is_change_bar=Value(c_bool, False)     #whether user has dragged the slider,default: False

        self.frame_index= Value('i',0)
        self.share_lock=Lock()  #shared lock for frame_index
        self.share_lock2 = Lock()  # shared lock for frame_index

        self.mutex = threading.Lock()


        self.timer = QTimer(self)  # used for the updating of progress bar
        self.temp_timer=QTimer(self)  #used for detecting whether the frame_total is given.
        self.frame_total = Value('i', -1)
        self.playable=Value(c_bool, True)
        self.is_working = Value(c_bool, False)
        manager=Manager()
        self.play_src = manager.Value(c_char_p, '0')             #用于记录播放的视频地址
        self.mode = None                # 'online' or 'offline'

    def init_connect(self):
        self.btn_pause.clicked.connect(self.pause)
        self.btn_close.clicked.connect(self.close)
        self.btn_start.clicked.connect(self.play)

    def init_offline_connect(self):

        self.timer.timeout.connect(self.update_progressBar)
        self.timer.start(50)  # update the progressbar value every 50ms
        self.temp_timer.timeout.connect(self.set_MaxValue)
        self.temp_timer.start(50)

        #progressbar
        self.progressBar.sliderPressed.connect(self.lockBar) # when the user is dragging the slider, stop updating the value
        self.progressBar.sliderReleased.connect(self.change_progressBar)


    def init_online_connect(self):
        pass
        


    def init_process(self):
        self.origin_img_q=mp.Queue(maxsize=2)
        self.result_img_q=mp.Queue(maxsize=4)
        self.p_detector = Process(target=detector,args = (self.origin_img_q,self.result_img_q))
        self.p_detector.start()
        self.img_fetcher=Process(target=play,args = (self.origin_img_q,self.frame_index,self.share_lock,self.frame_total,self.is_change_bar,self.playable,self.is_working,self.play_src))
        self.img_fetcher.start()


    def lockBar(self):
        self.share_lock.acquire()
        self.mutex.acquire()
        self.semaphore=False
        self.mutex.release()



    def change_progressBar(self):

        self.frame_index.value=self.progressBar.value()
        self.is_change_bar.value=True
        self.share_lock.release()
        self.mutex.acquire()
        self.semaphore=True
        self.mutex.release()

    def set_MaxValue(self):

        if self.frame_total.value is not -1:                    #只执行一次
            self.progressBar.setMaximum(self.frame_total.value)
            self.temp_timer.disconnect()

    def update_progressBar(self):
        self.mutex.acquire()
        if self.semaphore:
           self.progressBar.setValue(self.frame_index.value)
        self.mutex.release()

    def close(self):
        self.is_working.value=False
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        time.sleep(0.1)
        self.label_info.setText('空闲')

    def play(self):
        self.playable.value = True
        temp_str = self.label_info.text()
        if '[暂停]' in temp_str:
            temp_str =temp_str.replace('[暂停]','')
        self.label_info.setText(temp_str)
    def pause(self):
        self.playable.value=False
        temp_str=self.label_info.text()
        if '[暂停]' not in temp_str:
            temp_str='[暂停]'+temp_str
        self.label_info.setText(temp_str)

    def display(self):
        while True:
            start_time=time.time()

            if self.is_working.value:
                self.external_mutex.acquire()
                if not self.result_img_q.empty():
                    prev = time.time()
                    show=self.result_img_q.get()
                    post = time.time()
                    # print(datetime.timedelta(seconds=post - prev))

                    showImage = QImage(show.data, show.shape[1], show.shape[0],
                                       QImage.Format_RGB888)  # 转换成QImage类型
                    self.label_screen.setScaledContents(True)

                    self.label_screen.setPixmap(QPixmap.fromImage(showImage))  #
                    print("FPS: ", 1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop

                self.external_mutex.release()

            else:
                time.sleep(0.1)


    def init_offline(self,video_path=None):
        """

        :param video_path:  要离线播放的video地址
        :return:
        """

        self.init_offline_connect()

        self.offline_video_thread = threading.Thread(target=self.display)
        self.offline_video_thread.start()

    def start_online(self,play_src):
        self.play_src.value=play_src            #path of online camera
        play_src='0'
        self.label_info.setText('[在线模式]:'+play_src)
        self.is_working.value=True
        self.playable.value=True
        # for i in self.bottom_widgets:  # delete all the left_widgets and then replace them with new ones
        #     i.setVisible(False)
        #     self.layout1.removeWidget(i)
        # self.layout1.addWidget(self.btn_start, 8, 2, 1, 1)
        # self.layout1.addWidget(self.btn_pause, 8, 4, 1, 1)
        # self.btn_start.setVisible(True)
        # self.btn_pause.setVisible(True)
        self.progressBar.setVisible(False)


    def restart_online(self,play_src):
        self.play_src.value=play_src
        play_src = '0'
        self.is_working.value = False
        self.playable.value = False
        self.label_info.setText('[在线模式]:' + play_src)
        self.progressBar.setVisible(False)
        time.sleep(0.1)
        self.is_working.value = True
        self.playable.value = True


    def start_offline(self,play_src):
        self.play_src.value = play_src  # path of online camera
        self.label_info.setText('[离线模式]:' + play_src)
        self.is_working.value = True
        self.playable.value = True
        self.progressBar.setVisible(True)

    def restart_offline(self,play_src):
        self.play_src.value=play_src
        self.is_working.value = False
        self.playable.value = False
        self.label_info.setText('[离线模式]:' + play_src)
        self.progressBar.setVisible(True)
        time.sleep(0.1)
        self.is_working.value = True
        self.playable.value = True




