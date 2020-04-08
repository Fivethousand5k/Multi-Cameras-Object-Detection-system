from MyDetector import Helmet_Detector
import threading
import multiprocessing as mp
from multiprocessing import Process
import time
import subprocess
import cv2
import numpy




def detector(origin_img_q=None,result_img_q=None):
    helmet_detector=Helmet_Detector()
    while True:
        while origin_img_q.qsize() == 0:
            print("no")
        origin_img =origin_img_q.get()
        result_img=helmet_detector.detect(origin_img)
        result_img_q.put(result_img)






def play(q_put,playable=True,mode='offline',video_path='offline_videos/workers.mov'):
    videocap = cv2.VideoCapture(video_path)
    # videocap.set(cv2.CAP_PROP_POS_FRAMES,3000)
    frame_total = videocap.get(7)         #得到总帧数
    current_index=0
    while True:
        while not playable:
            time.sleep(0.1)
            print("sleeping")
        while playable:  # 点击pause按钮时，playable会被设置成False
            flag, frame = videocap.read()
            # time.sleep(self.interval)
            if flag:    # The frame is ready and already captured
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                time.sleep(0.05)
                # show = cv2.resize(frame, (int(self.label_screen.width() * 0.5), int(self.label_screen.height() * 0.5)),
                #                    interpolation=cv2.INTER_AREA)
                q_put.put(show)
                q_put.get() if q_put.qsize()>1 else None

                current_index+=1                #frame_index +1
            else:  # 如果当前视频播放完毕
                current_index = 0
                print("flag false")
                # playable=False
                # break






if __name__ == '__main__':
    mp.set_start_method(method='spawn')

    p=Process(target=detector)
    p.start()
