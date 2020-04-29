from MyDetector import Helmet_Detector
from MyDetector2 import Helmet_Detector2
import threading
import multiprocessing as mp
from multiprocessing import Process
import time
import subprocess
import cv2
import numpy




def detector(origin_img_q=None,result_img_q=None):
    helmet_detector=Helmet_Detector2()
    while True:
        while origin_img_q.qsize() == 0:
            print("no")
        origin_img =origin_img_q.get()
        result_img=helmet_detector.detect(origin_img)
        result_img_q.put(result_img)






def play(q_put,frame_index,share_lock,frame_total,is_change_bar,playable,mode='offline',video_path='offline_videos/workers2.mp4'):
    videocap = cv2.VideoCapture('offline_videos/workers.mov')
    frame_total.value = int(videocap.get(7))     #得到总帧数
    print(frame_total.value )
    while True:
        while not playable.value:
            time.sleep(0.1)
            print("sleeping")
        while playable.value:  # 点击pause按钮时，playable会被设置成False
            if is_change_bar.value: # when frame_index has been altered by the sliderbar
                 videocap.set(cv2.CAP_PROP_POS_FRAMES,frame_index.value)
                 is_change_bar.value=False
            flag, frame = videocap.read()
            # time.sleep(self.interval)
            if flag:    # The frame is ready and already captured
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                time.sleep(0.05)
                # show = cv2.resize(frame, (int(self.label_screen.width() * 0.5), int(self.label_screen.height() * 0.5)),
                #                    interpolation=cv2.INTER_AREA)
                q_put.put(show)
                q_put.get() if q_put.qsize()>1 else None
                share_lock.acquire()
                frame_index.value+=1
                share_lock.release()



            else:  # 如果当前视频播放完毕
                current_index = 0
                print("flag false")
                # playable=False
                # break






if __name__ == '__main__':
    mp.set_start_method(method='spawn')

    p=Process(target=detector)
    p.start()
