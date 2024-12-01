from ctypes import *
import math
import cv2
import numpy as np
import time
import darknet
from itertools import combinations

# Parameters
max_x_distance = 50
max_y_distance = 15
max_distance = math.sqrt(max_x_distance**2 + max_y_distance**2)
min_crowd_count_qualifier = 6
max_number_of_crowd_count = 0

# Configurations
configs = {
    # Active configuration
    "crowdhuman_v6": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-6.cfg",
        "weightPath": "./trained/yolov4/Training_9_[28_04_2021]/yolov4-custom-crowdhuman-tf-6_best.weights"
    },
    
    # Alternative configurations
    "crowdhuman_v5": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-5.cfg",
        "weightPath": "./trained/yolov4/Training_7_[26_04_2021]/yolov4-custom-crowdhuman-tf-5_best.weights"
    },
    "crowdhuman_v4": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-4.cfg",
        "weightPath": "./trained/yolov4/Training_8_[25_04_2021]/yolov4-custom-crowdhuman-tf-4_best_7.weights"
    },
    "crowdhuman_v3": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-3.cfg",
        "weightPath": "./trained/yolov4/Training_6_[25_04_2021]/yolov4-custom-crowdhuman-tf-3_best.weights"
    },
    "crowdhuman_v7": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-7.cfg",
        "weightPath": "./trained/yolov4/Training_10_[03_05_2021]/yolov4-custom-crowdhuman-tf-7_best.weights"
    },
    "crowdhuman_v2": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-2.cfg",
        "weightPath": "./trained/yolov4/Training_5_[25_04_2021]/yolov4-custom-crowdhuman-tf-2_best.weights"
    },
    "crowdhuman_v1": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-tf-1.cfg",
        "weightPath": "./trained/yolov4/Training_4_[24_04_2021]/yolov4-custom-crowdhuman-tf-1_best.weights"
    },
    "crowdhuman_v0": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/custom-yolov4-detector.cfg",
        "weightPath": "./trained/yolov4/Training_0_[23_03_2021]/custom-yolov4-detector_best.weights"
    },
    "vgg16_crowdhuman_v3": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-custom-crowdhuman-vgg16-3.cfg",
        "weightPath": "./trained/vgg16-yolov4/yolov4-custom-crowdhuman-vgg16-3_best.weights"
    },
    "tiny_crowdhuman_v1": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-tiny-custom-crowdhuman-1.cfg",
        "weightPath": "./trained/yolov4_tiny/Training_1_[30_03_2021]/yolov4-tiny-custom-crowdhuman-1_best.weights"
    },
    "tiny_crowdhuman_v2": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-tiny-custom-crowdhuman-2.cfg",
        "weightPath": "./trained/yolov4_tiny/Training_2_[22_04_2021]/yolov4-tiny-custom-crowdhuman-2_best.weights"
    },
    "tiny_crowdhuman_v3": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-tiny-custom-crowdhuman-3.cfg",
        "weightPath": "./trained/yolov4_tiny/Training_3_[23_04_2021]/yolov4-tiny-custom-crowdhuman-3_best.weights"
    },
    "tiny_crowdhuman_v4": {
        "metaPath": "./Dataset/Crowdhuman/yolo_crowdhuman.data",
        "configPath": "./cfg/yolov4-tiny-custom-crowdhuman-4.cfg",
        "weightPath": "./trained/yolov4_tiny/Training_4_[24_04_2021]/yolov4-tiny-custom-crowdhuman-4_best_13.weights"
    }
}

def select_config(config_key):
    """Select the configuration based on the provided key."""
    if config_key in configs:
        return configs[config_key]
    raise ValueError(f"Invalid configuration key: {config_key}")

# Utility Functions
def is_close(p1, p2):
    return math.sqrt(p1**2 + p2**2)

def convert_back(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def draw_boxes(detections, img):
    global max_number_of_crowd_count, max_distance
    if not detections:
        return img

    centroid_dict = {}
    for objectId, detection in enumerate(detections):
        name_tag = str(detection[0])
        if name_tag == 'person':
            x, y, w, h = detection[2]
            xmin, ymin, xmax, ymax = convert_back(x, y, w, h)
            centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax)

    red_zone_list = []
    red_line_list = []
    new_red_zone_list = {}

    for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2):
        dx, dy = p1[0] - p2[0], p1[1] - p2[1]
        distance = is_close(dx, dy)
        if distance < max_distance:
            for ids in new_red_zone_list:
                if id1 in new_red_zone_list[ids] or id2 in new_red_zone_list[ids]:
                    new_red_zone_list[ids].extend([id1, id2])
                    break
            else:
                new_red_zone_list[len(new_red_zone_list)] = [id1, id2]
            red_line_list.append(p1[0:2])
            red_line_list.append(p2[0:2])
            red_zone_list.extend([id1, id2])

    for idx, box in centroid_dict.items():
        color = (255, 0, 0) if idx in red_zone_list else (0, 255, 0)
        cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), color, 2)

    for check in range(0, len(red_line_list) - 1, 2):
        cv2.line(img, red_line_list[check], red_line_list[check + 1], (255, 0, 0), 2)

    return img

# Main YOLO Function
def YOLO(config_key="crowdhuman_v6"):
    global metaMain, netMain, altNames

    config = select_config(config_key)
    metaMain = darknet.load_meta(config["metaPath"].encode("ascii"))
    netMain = darknet.load_net_custom(config["configPath"].encode("ascii"), config["weightPath"].encode("ascii"), 0, 1)
    altNames = None

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = darknet.detect_image(netMain, metaMain, frame_rgb, thresh=0.25)
        frame = draw_boxes(detections, frame)
        cv2.imshow('YOLO Detection', frame)
        if cv2.waitKey(1) == 27:  # Press Esc to exit
            break
    cap.release()
    cv2.destroyAllWindows()