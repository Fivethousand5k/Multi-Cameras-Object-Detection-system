from MyDetector2 import Helmet_Detector2
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
def save(label_dir,img_name,img,detections):


    txt_path = os.path.join(label_dir, img_name + '.txt')
    label_txt = open(txt_path, 'w')
    if detections is not None:
        for x1, y1, x2, y2, conf, cls_pred in detections:
            img_height, img_width, channels = img.shape
            center_x = float(((x1 + x2) / 2) / img_width)
            center_y = float(((y1 + y2) / 2) / img_height)
            width = float((x2 - x1) / img_width)
            height = float((y2 - y1) / img_height)
            if center_x<=0 or center_y <=0 or width<=0 or height <=0:
                print("break")
                continue
            label = int(cls_pred)
            output = [str(label), str(round(center_x,4)), str(round(center_y,4)), str(round(width,4)), str(round(height,4))]
            temp_str = " ".join(output)
            label_txt.write(temp_str + '\n')
    label_txt.close()

def save2(label_dir,img_name,img,detections):

    txt_path = os.path.join(label_dir, img_name + '.txt')
    label_txt = open(txt_path, 'w')
    if detections is not None:
        for x1, y1, x2, y2, conf, cls_pred in detections:
            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)
            conf=float(conf)
            if x1<=0 or y1<=0 or x2<=0 or y2<=0:
                print("break")
                continue
            label = names[int(cls_pred)]
            output = [str(label),str(round(conf,3)),str(round(x1,2)), str(round(y1,2)), str(round(x2,2)), str(round(y2,2))]
            temp_str = " ".join(output)
            label_txt.write(temp_str + '\n')
    label_txt.close()


def play():

    save_dataset_dir='E:\Datasets\Safety-helmet-test-dataset'   #under this dir, initially, there is only one sub dir named imgs
    imgs_dir=os.path.join(save_dataset_dir,'imgs')
    labels_dir=os.path.join(save_dataset_dir,'labels2')  #label file generated would be saved there
    if not os.path.exists(labels_dir):
        os.mkdir(labels_dir)
    imgs_list=sorted(os.listdir(imgs_dir))
    imgs_list=['test_000041.jpg']
    print(imgs_list)
    helmet_detector = Helmet_Detector2()


    # videocap.set(cv2.CAP_PROP_POS_FRAMES,3000)

    for img in imgs_list:
        print(img)
        img_name=img[0:-4]
        img_path=os.path.join(imgs_dir,img)
        img= cv2.imread(img_path)
        # time.sleep(self.interval)
        save_tag=True
        detections = helmet_detector.get_label_and_pos(img)
        if save_tag:
            save2(label_dir=labels_dir,img_name=img_name,img=img,detections=detections)


play()