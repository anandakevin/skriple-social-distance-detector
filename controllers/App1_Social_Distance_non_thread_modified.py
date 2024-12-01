#================================================================
#  To learn how to Develop Advance YOLOv4 Apps - Then check out:
#  https://augmentedstartups.info/yolov4release
#================================================================ 
from ctypes import *
import math
import random
import os
import cv2
import sys
import numpy as np
import time
import darknet
# from imutils.video import FileVideoStream
from itertools import combinations

max_x_distance = 50
max_y_distance = 15
max_distance = 80
min_crowd_count = 3
max_number_of_crowd_count = 0

def make_1080p(cap):
    cap.set(3, 1920)
    cap.set(4, 1080)

def make_720p(cap):
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p(cap):
    cap.set(3, 640)
    cap.set(4, 480)

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def is_close(p1, p2):
    """
    #================================================================
    # 1. Purpose : Calculate Euclidean Distance between two points
    #================================================================    
    :param:
    p1, p2 = two points for calculating Euclidean Distance

    :return:
    dst = Euclidean Distance between two 2d points
    """
    dst = math.sqrt(p1**2 + p2**2)
    #=================================================================#
    return dst 


def convertBack(x, y, w, h): 
    #================================================================
    # 2.Purpose : Converts center coordinates to rectangle coordinates
    #================================================================  
    """
    :param:
    x, y = midpoint of bbox
    w, h = width, height of the bbox
    
    :return:
    xmin, ymin, xmax, ymax
    """
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    # print("Detections: ", detections) 
    """
    :param:
    detections = total detections in one frame
    img = image from detect_image method of darknet

    :return:
    img with bbox
    """
    #================================================================
    # 3.1 Purpose : Filter out Persons class from detections and get 
    #           bounding box centroid for each person detection.
    #================================================================
    if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
        centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
        objectId = 0								# We inialize a variable called ObjectId and set it to 0
        for detection in detections:				# In this if statement, we filter all the detections for persons only
            # new
            detectionNew = (detection[0], float(detection[1]), detection[2])
            
            # Check for the only person name tag 
            name_tag = str(detectionNew[0])   # Coco file has string of all the names
            if name_tag == 'person':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]      	# Store the center points of the detections
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
                # Append center point of bbox for persons detected.
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
                objectId += 1 #Increment the index for each detection      
    #=================================================================#
        # print('total people detected: ', len(centroid_dict))
        # print(centroid_dict)
    #=================================================================
    # 3.2 Purpose : Determine which person bbox are close to each other
    #=================================================================            	
        red_zone_list = [] # List containing which Object id is in under threshold distance condition. 
        red_line_list = []

        new_red_zone_list = dict()

        for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2): # Get all the combinations of close detections, #List of multiple items - id1 1, points 2, 1,3
            dx, dy = p1[0] - p2[0], p1[1] - p2[1]  	# Check the difference between centroid x: 0, y :1
            
            distance = is_close(dx, dy) 			# Calculates the Euclidean distance
            firstIdx = -1
            secIdx = -1
            if distance < max_distance:				# Set our social distance threshold - If they meet this condition then..
                for ids in new_red_zone_list:
                    if id1 in new_red_zone_list[ids] and firstIdx == -1:
                        firstIdx = ids
                    if id2 in new_red_zone_list[ids] and secIdx == -1:
                        secIdx = ids
                    if firstIdx != -1 and secIdx != -1:
                        break

                # print(id1, ' ', id2, ' ', firstIdx, ' ', secIdx)

                if firstIdx != -1 and secIdx != -1 and firstIdx != secIdx: 
                    new_red_zone_list[min(firstIdx, secIdx)] = new_red_zone_list[firstIdx] + new_red_zone_list[secIdx]
                    del new_red_zone_list[max(firstIdx, secIdx)]
                elif firstIdx != -1:
                    if id2 not in new_red_zone_list[firstIdx]:
                        new_red_zone_list[firstIdx].append(id2)
                elif secIdx != -1:
                    if id1 not in new_red_zone_list[secIdx]:
                        new_red_zone_list[secIdx].append(id1)
                else:
                    new_red_zone_list[len(new_red_zone_list)] = [id1, id2]

                # print("red_zone_list", red_zone_list)
                # print("new_red_zone_list", new_red_zone_list)
                    

                red_line_list.append(p1[0:2])
                red_line_list.append(p2[0:2])

                if id1 not in red_zone_list:
                    red_zone_list.append(id1)       #  Add Id to a list
                    # red_line_list.append(p1[0:2])   #  Add points to the list
                if id2 not in red_zone_list:
                    red_zone_list.append(id2)		# Same for the second id 
                    # red_line_list.append(p2[0:2])
        
        for idx, box in centroid_dict.items():      # dict (1(key):red(value), 2 blue)  idx - key  box - value
            if idx in red_zone_list:   # if id is in red zone list
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes << format: RGB
                # cv2.rectangle(image, start_point, end_point, color, thickness)
		#=================================================================#

        # print("Final Result: ", new_red_zone_list)
		#=================================================================
    	# 3.3 Purpose : Display Risk Analytics and Show Risk Indicators
    	#=================================================================        
        ttlRedPeople = "People at Risk: %s" % str(len(red_zone_list)) 			# Count People at Risk
        ttlGroup = "Number of groups: %s" % str(len(new_red_zone_list))
        crowdCount = 0
        # print("red_zone_list ", red_zone_list)
        # print("new_red_zone_list", new_red_zone_list)
        for idx in new_red_zone_list:
            # print("jumlah orang: ", len(new_red_zone_list[idx]), ", orang2nya: ", new_red_zone_list[idx])
            if len(new_red_zone_list[idx]) > min_crowd_count:
                crowdCount += 1
        # print("crowdCount: ", crowdCount)

        ttlCrowd = "Number of crowd consisting of at least %s people: %d" % (str(min_crowd_count), crowdCount)
        
        global max_number_of_crowd_count
        max_number_of_crowd_count = max(crowdCount, max_number_of_crowd_count)
        maxNumberOfCrowdCount = "Max Number of crowd consisting of at least %s people: %d" % (str(min_crowd_count), max_number_of_crowd_count)
        
        location1 = (10,25)												# Set the location of the displayed text
        location2 = (10,60)												# Set the location of the displayed text
        location3 = (10,95)												# Set the location of the displayed text
        location4 = (10,130)												# Set the location of the displayed text
        
        cv2.putText(img, ttlRedPeople, location1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
        cv2.putText(img, ttlRedPeople, location1, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text
        
        cv2.putText(img, ttlGroup, location2, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
        cv2.putText(img, ttlGroup, location2, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text
        
        cv2.putText(img, ttlCrowd, location3, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
        cv2.putText(img, ttlCrowd, location3, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text
        
        cv2.putText(img, maxNumberOfCrowdCount, location4, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
        cv2.putText(img, maxNumberOfCrowdCount, location4, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text

        # print(red_line_list)
        for check in range(0, len(red_line_list)-1):					# Draw line between nearby bboxes iterate through redlist items
            start_point = red_line_list[check] 
            end_point = red_line_list[check+1]
            check_line_x = abs(end_point[0] - start_point[0])   		# Calculate the line coordinates for x  
            check_line_y = abs(end_point[1] - start_point[1])			# Calculate the line coordinates for y
            # if (check_line_x < max_x_distance) and (check_line_y < max_y_distance):				# If both are We check that the lines are below our threshold distance.
            if (is_close(check_line_x, check_line_y) < max_distance):				# If both are We check that the lines are below our threshold distance.
                cv2.line(img, start_point, end_point, (255, 0, 0), 2)   # Only above the threshold lines are displayed. 
            # (Red, Green, Blue, Line Thickness)
        #=================================================================#
    return img


netMain = None
metaMain = None
altNames = None


def YOLO():
    """
    Perform Object detection
    """
    global metaMain, netMain, altNames
    configPath = "./cfg/yolov4.cfg"
    weightPath = "./Models/yolov4.weights"
    metaPath = "./cfg/coco.data"

    # configPath = "./cfg/yolov4-custom.cfg"
    # weightPath = "./backup/CrowdHuman/Training #1 [31-01-2021] yolov4 normal/custom-yolov4-detector_final.weights"
    # weightPath = "./backup/yolov3-tiny-crowdhuman_last.weights"
    # E:/Projects/skripsi/alexeyb_darknet_cuda_working_by_vs/build/darknet/x64/backup/CrowdHuman/Training #1 [29-03-2021] yolov4 normal from zero
    # configPath = "./cfg/yolov4-custom-crowdhuman-1.cfg"
    # weightPath = "./backup/CrowdHuman/Training_#1_[23-03-2021]/yolov4-custom-crowdhuman-1_final.weights"
    # metaPath = "./Dataset/Crowdhuman/yolo_crowdhuman.data"
    
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("./Input/video3.mp4")
    # cap = cv2.VideoCapture("rtsp://:8554/realtime.avi")
    # cap = cv2.VideoCapture("rtsp://localhost:8554//realtime.mp4")
    # cap = cv2.VideoCapture("rtsp://localhost:8554/")
    # cap = FileVideoStream("./Input/video3.mp4").start()
    # make_720p()
    change_res(cap, 1280, 720)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # frame_width = int(cap.stream.get(3))
    # frame_height = int(cap.stream.get(4))
    new_height, new_width = frame_height // 2, frame_width // 2
    print("Video Resolution:",frame_width, ' ', frame_height)
    ori_fps = cap.get(cv2.CAP_PROP_FPS)
    print(ori_fps)
    # print("Original Video FPS:", ori_fps)
    #.avi > MJPG
    #.mp4 > MPAV
    # out = cv2.VideoWriter(
    #         "./Output/video3_output.avi", cv2.VideoWriter_fourcc(*"MJPG"), ori_fps,
    #         (frame_width, frame_height))
    out = cv2.VideoWriter(
            "./Output/video3_output.mp4", cv2.VideoWriter_fourcc(*"MPAV"), ori_fps,
            (frame_width, frame_height))
    
    # print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(frame_width, frame_height, 3)
    num_of_frames = 0
    min_fps = 1000
    max_fps = 0
    fps_count = 0
    total_fps = 0

    while True:
    # while cap.more():
        num_of_frames += 1
        # print('Frame: ', num_of_frames)
        prev_time = time.time()
        ret, frame_read = cap.read()
        # frame_read = cap.read()
        # Check if frame present :: 'ret' retur/ns True if frame present, otherwise break the loop.
        if not ret:
            break
        # if frame_read is None:
        #     break

        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (frame_width, frame_height),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        # old
        # detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
        # new
        detections = darknet.detect_image(netMain, altNames, darknet_image, thresh=0.25)
        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        fps = 1/(time.time()-prev_time)
        processing_time = (time.time()-prev_time)*100
        # print('FPS:', fps)
        # print('Frame Detected in:', processing_time, 'ms')
        min_fps = min(min_fps, fps)
        max_fps = max(max_fps, fps)
        fps_count += 1
        total_fps += fps
        cv2.imshow('Output', image)
        # sys.stdout.buffer.write(image.tobytes())
        # sys.stdout.write(image.tostring())
        cv2.waitKey(3)
        out.write(image)

    cap.release()
    # cap.stop()
    out.release()
    avg_fps = total_fps / fps_count
    # print("Min FPS:", min_fps)
    # print("Max FPS:", max_fps)
    # print("Average FPS:", avg_fps)
    # print(":::Video Write Completed")

if __name__ == "__main__":
    YOLO()
