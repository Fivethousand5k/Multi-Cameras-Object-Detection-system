from MyDetector2 import Helmet_Detector2
import threading
import multiprocessing as mp
from multiprocessing import Process
import datetime
import subprocess
import cv2
import numpy as np
import os
import time


names=['hat','person']
colors=[[144, 238, 144],[220,20,60]]
def save(dataset_dir,img_name,img,detections):
    imgs_dir=os.path.join(dataset_dir,'imgs')
    labels_dir = os.path.join(dataset_dir, 'labels')
    imgfile_name=os.path.join(imgs_dir,img_name+'.jpg')

    if not os.path.exists( imgs_dir):
        os.mkdir(imgs_dir)
    if not os.path.exists(labels_dir):
        os.mkdir(labels_dir)
    txt_path = os.path.join(labels_dir, img_name + '.txt')
    label_txt = open(txt_path, 'w')
    for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
        img_height, img_width, channels = img.shape
        center_x = float(((x1 + x2) / 2) / img_width)
        center_y = float(((y1 + y2) / 2) / img_height)
        width = float((x2 - x1) / img_width)
        height = float((y2 - y1) / img_height)
        label = int(cls_pred)
        output = [str(label), str(round(center_x,4)), str(round(center_y,4)), str(round(width,4)), str(round(height,4))]
        temp_str = " ".join(output)
        label_txt.write(temp_str + '\n')
    label_txt.close()
    cv2.imwrite(imgfile_name,img)


def play():



    videocap = cv2.VideoCapture('offline_videos/workers.mov')
    helmet_detector = Helmet_Detector2()
    window_name="video"
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    # videocap.set(cv2.CAP_PROP_POS_FRAMES,3000)
    count=121
    save_prev_time=datetime.datetime.now()
    while True:  # 点击pause按钮时，playable会被设置成False
        start_time=time.time()
        flag, frame = videocap.read()
        # time.sleep(self.interval)
        if flag:  # The frame is ready and already captured
            # frame=helmet_detector.detect(frame)


            cv2.imshow(window_name, frame)
            print("FPS: ", 1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop
            cv2.waitKey(1)


        else:  # 如果当前视频播放完毕
            break

            # playable=False
            # break

play()