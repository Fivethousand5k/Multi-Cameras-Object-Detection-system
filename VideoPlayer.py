import cv2
from PyQt5.Qt import *
from PyQt5 import QtWidgets
from MyDetector import Helmet_Detector
import threading
import  cv2
import  time
import  datetime
class Player(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.init_UI()
        self.init_data()
        # self.init_offline()

    def init_UI(self):
        self.label_screen = QtWidgets.QLabel(self)  # 用于展示图片的label
        self.label_screen.setPixmap(QPixmap("GUI/resources/yellowwhite.jfif"))

    def init_data(self):
        self.helmet_detector=Helmet_Detector()


    def init_offline(self,video_path):
        """

        :param video_path:  要离线播放的video地址
        :return:
        """
        self.timer = QTimer(self)           #计时器，用于以线程方式定时唤醒播放
        self.offline_video_thread = threading.Thread(target=self.play_offline)
        self.offline_videocap= None
        self.offline_path=video_path
        self.playable=True  #是否可以播放，用它来控制离线播放的开始和暂停
        self.frame_total=None          #当前播放视频的总帧数
        self.current_index=0   #当前播放的帧号
        self.offline_video_thread.start()


    def play_offline(self):
        # self.offline_videocap = cv2.VideoCapture(self.offline_path)
        self.offline_videocap = cv2.VideoCapture(0)
        self.frame_total = self.offline_videocap.get(7)         #得到总帧数
        while self.playable:  # 点击pause按钮时，playable会被设置成False
            prev_time = time.time()
            flag, frame = self.offline_videocap.read()
            # time.sleep(self.interval)
            if flag:    # The frame is ready and already captured
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                prev_time = time.time()
                show=self.helmet_detector.detect(show)
                # show = cv2.resize(frame, (int(self.label_screen.width() * 0.5), int(self.label_screen.height() * 0.5)),
                #                    interpolation=cv2.INTER_AREA)
                showImage = QImage(show.data, show.shape[1], show.shape[0],
                                   QImage.Format_RGB888)  # 转换成QImage类型
                self.label_screen.setScaledContents(True)

                self.label_screen.setPixmap(QPixmap.fromImage(showImage))  # 图像输出至label
                self.current_index+= 1

            else:  # 如果当前视频播放完毕
                self.current_index = 0
                break
            post_time = time.time()
            print(datetime.timedelta(seconds=post_time - prev_time))
        if not self.playable:                   #如果 self.playable为false（例如按了暂停键后），线程在这里会结束
            QApplication.processEvents()  # end while self.playable:




