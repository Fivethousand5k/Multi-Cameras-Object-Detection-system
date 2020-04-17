from __future__ import division

from helmet_detector.models import *
from helmet_detector.utils.utils import *

import os
import sys
import time
import datetime
import argparse

from PIL import Image

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable
import cv2
import torchvision.transforms as transforms
import torch.nn.functional as F
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

model_def = "helmet_detector/config/yolov3-custom.cfg"  # 模型的config
img_size = 416  # size of each image dimension
weights_path = "helmet_detector/checkpoints/yolov3_ckpt_310.pth"  # checkpoint
class_path = "helmet_detector/data/custom/classes.names"            #类别文件
conf_thres=0.9          #object confidence threshold
nms_thres=0.4             #iou thresshold for non-maximum suppression
names=['hat','person']
colors=[[144, 238, 144],[220,20,60]]

class Helmet_Detector():
    def __init__(self):
        self.test_no_model=True
        if not self.test_no_model:
            self.device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
            print("using",self.device)
            classes = load_classes(class_path)  # Extracts class labels from file
            self.model= Darknet(model_def, img_size=img_size).to(self.device)
            self.model.load_state_dict(torch.load(weights_path))         #装载训练参数
            self.model.eval()                   #set in eval mode

    def transform_to_tensor(self,img):

        img = transforms.ToTensor()(img)
        # Pad to square resolutio
        img, _ = pad_to_square(img, 0)
        # Resize
        img = resize(img, img_size)
        img=torch.stack([img], 0, out=None)
        # pre_time = time.time()
        img = Variable(img.type(self.Tensor))
        # post_time = time.time()

        # print(datetime.timedelta(seconds=post_time - pre_time))

        return img



    def detect(self,input_img):

        # img to tensor
        assert isinstance(input_img, np.ndarray), "input must be a numpy array!"

        if not self.test_no_model:
            tensor_img=self.transform_to_tensor(input_img)

            # Get detections
            prev_time = time.time()
            with torch.no_grad():
                detections = self.model(tensor_img)
                detections = non_max_suppression(detections, conf_thres, nms_thres)

            if detections[0] is not None:
                # Rescale boxes to original image
                detections = rescale_boxes(detections[0], img_size, input_img.shape[:2])
                unique_labels = detections[:, -1].cpu().unique()
                n_cls_preds = len(unique_labels)
                # bbox_colors = random.sample(colors, n_cls_preds)
                for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
                    cv2.rectangle(input_img, (x1, y1), (x2, y2), colors[int(cls_pred)], 10)
                    cv2.putText(input_img, names[int(cls_pred)], (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 3, colors[int(cls_pred)], 2)

            post_time = time.time()
            print(datetime.timedelta(seconds=post_time - prev_time))
        return input_img

                # plt.text(
                #     x1,
                #     y1,
                #     s=classes[int(cls_pred)],
                #     color="white",
                #     verticalalignment="top",
                #     bbox={"color": color, "pad": 0},
                # )


    def get_label_and_pos(self,input_img):
        assert isinstance(input_img, np.ndarray), "input must be a numpy array!"
        tensor_img = self.transform_to_tensor(input_img)

        # Get detections
        prev_time = time.time()
        with torch.no_grad():
            detections = self.model(tensor_img)
            detections = non_max_suppression(detections, conf_thres, nms_thres)

        if detections[0] is not None:
            # Rescale boxes to original image
            detections = rescale_boxes(detections[0], img_size, input_img.shape[:2])
            # unique_labels = detections[:, -1].cpu().unique()
            # n_cls_preds = len(unique_labels)
            # bbox_colors = random.sample(colors, n_cls_preds)
            # for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
                # cv2.rectangle(input_img, (x1, y1), (x2, y2), colors[int(cls_pred)], 10)
                # cv2.putText(input_img, names[int(cls_pred)], (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 3,
                #             colors[int(cls_pred)], 2)


        return detections


def pad_to_square(img, pad_value):
    c, h, w = img.shape
    dim_diff = np.abs(h - w)
    # (upper / left) padding and (lower / right) padding
    pad1, pad2 = dim_diff // 2, dim_diff - dim_diff // 2
    # Determine padding
    pad = (0, 0, pad1, pad2) if h <= w else (pad1, pad2, 0, 0)
    # Add padding
    img = F.pad(img, pad, "constant", value=pad_value)

    return img, pad

def resize(image, size):
    image = F.interpolate(image.unsqueeze(0), size=size, mode="nearest").squeeze(0)
    return image





