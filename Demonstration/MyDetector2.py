from __future__ import division
from helmet_detector2.models import *
from helmet_detector2.utils.utils import *
from helmet_detector2.utils.datasets import *

import os
import sys
import time
import datetime
import argparse

from PIL import Image

import torch
import cv2
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable
import torchvision.transforms as transforms
import torch.nn.functional as F

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

class_path='helmet_detector2/data/custom/classes.names'
model_def='helmet_detector2/cfg/yolov3-spp.cfg'
weights_path='helmet_detector2/weights/best_yolov3-ul.pt'
img_size=416
conf_thres=0.8          #object confidence threshold
nms_thres=0.4             #iou thresshold for non-maximum suppression
iou_thres=0.6
names=['hat','person']
colors = [[220,20,60],[25,25,112]]
class Helmet_Detector2():
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
        print("using", self.device)
        self.model = Darknet(model_def, img_size)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device)['model'])
        self.model.to(self.device).eval()

    def detect(self,input_img):
        img = [letterbox(input_img, new_shape=img_size, interp=cv2.INTER_LINEAR)[0]]
        # Stack
        img = np.stack(img, 0)
        img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device).float()
        img /= 255.0
        pred = self.model(img)[0]
        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        if pred[0] is not None:
            det=pred[0]
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], input_img.shape).round()
            for *xyxy, conf, cls in det:
                label = '%s %.2f' % (names[int(cls)], conf)
                plot_one_box(xyxy, input_img, label=label, color=colors[int(cls)])

        return input_img


def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = max(img1_shape) / max(img0_shape)  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2]] -= pad[0]  # x padding
    coords[:, [1, 3]] -= pad[1]  # y padding
    coords[:, :4] /= gain
    clip_coords(coords, img0_shape)
    return coords

def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

if __name__ == '__main__':
    detector=Helmet_Detector2()
    cap=cv2.VideoCapture(0)
    _,img=cap.read()
    detector.detect(img)