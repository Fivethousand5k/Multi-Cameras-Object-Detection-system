from MyDetector import Helmet_Detector
import threading
import multiprocessing as mp
from multiprocessing import Process
import datetime
import subprocess
import cv2
import numpy as np
import os


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
    dataset_dir='home-made-datasets/person_carrying_a_hat'   #under this dir, there are 2 sub dir: ' imgs' and ' labels'
    name_prefix="a"
    num=150   # collect 500 photos
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)



    videocap = cv2.VideoCapture(0)
    helmet_detector = Helmet_Detector()
    window_name="video"
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    # videocap.set(cv2.CAP_PROP_POS_FRAMES,3000)
    count=121
    save_prev_time=datetime.datetime.now()
    while True:  # 点击pause按钮时，playable会被设置成False
        flag, frame = videocap.read()
        # time.sleep(self.interval)
        if flag:  # The frame is ready and already captured
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
            origin_frame=np.copy(frame)
            detections=helmet_detector.get_label_and_pos(frame)
            save_tag=False
            if detections[0] is not None:
                for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
                    if int(cls_pred) is 0 and (datetime.datetime.now() - save_prev_time).seconds > 1:
                        save_tag=True
                    cv2.rectangle(frame, (x1, y1), (x2, y2), colors[int(cls_pred)], 10)
                    cv2.putText(frame, names[int(cls_pred)], (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 3,
                                colors[int(cls_pred)], 2)
                if save_tag:
                    save(dataset_dir=dataset_dir, img_name=name_prefix +"_"+str(count), img=origin_frame,
                         detections=detections)
                    count += 1
                    save_prev_time=datetime.datetime.now()
            cv2.putText(frame, "count:" + str(count), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        colors[0], 2)
            if count>num:
                temp_str="Having collected sufficient images"
                print(temp_str)
                classes_txt = open(os.path.join(dataset_dir,"labels", "classes.txt"), 'w')
                for name in names:
                    classes_txt.write(name + '\n')
                classes_txt.close()
                cv2.putText(frame, temp_str, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                            colors[0], 2)
                cv2.imshow(window_name, frame)
                break
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)

        else:  # 如果当前视频播放完毕
            break

            # playable=False
            # break

play()