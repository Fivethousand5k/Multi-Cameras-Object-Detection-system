import os
import time
import requests
import subprocess
import datetime

import cv2
import numpy as np
import tensorflow as tf
import multiprocessing as mp






def queue_img_put(q_put):
    cap = cv2.VideoCapture('E:\python-tasks\WHU-CSTECH\offline_videos\workers.mov')

    while True:
        is_opened, frame = cap.read()
        time.sleep(0.02)
        q_put.put(frame) if is_opened else None
        q_put.get() if q_put.qsize() > 1 else None


def queue_img_get(q_get, window_name="1"):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO) if window_name else None


    while True:
        prev = time.time()
        origin_img = q_get.get()
        post = time.time()
        print(datetime.timedelta(seconds=post - prev))
        img = np.copy(origin_img)
        (cv2.imshow(window_name, img), cv2.waitKey(1)) if window_name else None




def tf_model(origin_img_q, result_img_q):
            is_opened = True
            while is_opened:
                while origin_img_q.qsize() == 0:
                    time.sleep(0.1)
                origin_img = origin_img_q.get()  # one tf model

                img = np.copy(origin_img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                result_img_q.put(origin_img)





def run():
    mp.set_start_method(method='spawn')

    origin_img_q = mp.Queue(maxsize=2)
    result_img_q = mp.Queue(maxsize=4)
    origin_img_q2 = mp.Queue(maxsize=2)
    result_img_q2 = mp.Queue(maxsize=4)
    origin_img_q3 = mp.Queue(maxsize=2)
    result_img_q3 = mp.Queue(maxsize=4)

    processes = [
        mp.Process(target=queue_img_put, args=(origin_img_q, )),
        mp.Process(target=tf_model, args=(origin_img_q, result_img_q)),
        mp.Process(target=queue_img_get, args=(result_img_q,)),
        mp.Process(target=queue_img_put, args=(origin_img_q2,)),
        mp.Process(target=tf_model, args=(origin_img_q2, result_img_q2)),
        mp.Process(target=queue_img_get, args=(result_img_q2,)),
        # mp.Process(target=queue_img_put, args=(origin_img_q3,)),
        # mp.Process(target=tf_model, args=(origin_img_q3, result_img_q3)),
        # mp.Process(target=queue_img_get, args=(result_img_q3,)),
            ]


    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    [process.join() for process in processes]

if __name__ == '__main__':
    run()